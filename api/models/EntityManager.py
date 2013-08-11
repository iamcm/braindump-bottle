from decimal import Decimal
from bson.objectid import ObjectId
import datetime
from models import Logger 
from settings import DBDEBUG

class EntityManager:
    """
    This class handles getting a list of entities, or removing one/many entities
    from a mongo collection
    """
    def __init__(self, db):
        self.db = db
        
    def get_all(self, entity, filter_criteria='', sort_by=[], skip=None, limit=None, count=False):
        """
        Get all or a selection of entities from the datastore. This returns
        a list of entities.
        
        Entity should be class object
        
        filter_criteria can be used to filter the results and should be
        a dictionary that adheres to the pymongo documentation
        http://api.mongodb.org/python/current/genindex.html
        {'name':'jim'}
        
        sort_by should be a list of tuples (attribute, direction)
        [
            ('name',1),
            ('age',1),
        ]
        
        skip and limit are both ints and are used for pagination

        count should be True if only a count of the results is required

        e.g.
        todos = EntityManager(_DBCON).get_all(Todo
                                            ,filter_criteria={'userId':bottle.request.session.userId}
                                            ,sort_by=[('added', 1)]
                                            ,skip=20
                                            ,limit=10
                                            )
        collections = EntityManager(_DBCON).get_all(Item
                                , filter_criteria={
                                    'userId':bottle.request.session.userId,
                                    'collections':{
                                        '$in':[collectionId]
                                    },
                                    '$or':[
                                        {'title':'Public'},
                                        {'title':'An event'},                                                   
                                    ],
                                    'title':{'$regex':searchterm, '$options': 'i' },
                                })
        """
        extraCriteria = ''

        if len(sort_by)>0:
            extraCriteria += '.sort(%s)' % str(sort_by)

        if skip:
            extraCriteria += '.skip(%s)' % str(skip)

        if limit:
            extraCriteria += '.limit(%s)' % str(limit)

        if count:
            extraCriteria += '.count()'
            
        command = 'self.db.%s.find(%s)%s' % (entity.__name__
                                                ,str(filter_criteria)
                                                , extraCriteria
                                            )

        if DBDEBUG: Logger.log_to_file(command)

        if count:
            return eval(command)
        else:
            entities = []
            for result in eval(command):
                e = entity(self.db)
                e._hydrate(result)
                entities.append(e)
            
            return entities
        
    def delete_one(self, entity, _id):
        """
        Deletes a single entity from the datastore based on the id given
        
        entity should be a string
        _id should be the string entity id
        
        e.g.
        todoId = '5047b7bb37d5e64e9a4b1c74'
        EntityManager(_DBCON).delete_one('Todo', todoId)
        """
        command = 'self.db.%s.remove({"_id":ObjectId("%s")})' % (entity, str(_id))
        if DBDEBUG: Logger.log_to_file(command)
        eval(command)

    def _stem(self, word):
        parts = []

        for i in range(len(word)):
            try:
                parts.append(word[i:i+3])
            except:
                pass

        return [p for p in parts if len(p) > 2]

    def fuzzy_text_search(self, entity, searchterm, field):
        """
        Performs a fuzzy text search on a given entity.

        searchterm should be one or more space seperated words

        field should be a string naming a field to search

        e.g.
        searchterm = 'This is a test'
        items = EntityManager(_DBCON).fuzzy_text_search(Item, searchterm, 'title')        
        """
        matches = {} #for raw matches
        goodmatches = [] #for matches that are accurate

        # search a single word at a time
        for word in searchterm.split(' '):
            #split the word into parts
            stems = self._stem(word)
            #run a search for each part
            for term in stems:
                # construct mongo command to search for the part in the given field
                filter_criteria={field:{'$regex':term, '$options': 'i' }}

                command = 'self.db.%s.find(%s)' % (entity.__name__, str(filter_criteria))                    

                # add each result to the 'matches' list, or increment its count if it already exists
                for result in eval(command):
                    try:
                        matches[result[field]]['count'] += 1
                    except:
                        matches[result[field]] = {'entity':result, 'count':1}
    
            # if we have any stems
            if len(stems) > 0:
                # for each match calculate its accuracy and add it to the 'goodmatches' list if applicable
                for m, entity_count_dict in matches.items():
                    c = entity_count_dict['count']

                    """
                    if the percentage of stems that matched is greater than 70 
                    eg 'TIME' would stem to 'ti','im','me', so a search for 'tide' would only match two stems out of three
                    with a percentage of 66%
                    --OR--
                    the percentage of stems that matched is only 20% but the length of word that matched is the same or two characters
                    longer than the search word
                    eg the example above would pass now because i assume that the words are similar based on a partial stem match and a similar 
                    word length
                    """
                    if Decimal(c) / Decimal(len(stems)) * 100 > 70 \
                        or (len(m) < len(word)+2 and len(m) >= len(word) and Decimal(c) / Decimal(len(stems)) * 100 > 20):

                        """
                        this is a good match so add it to the list along with some weighting fields to order the results by. 

                        The first weight is the number of stems that this word matched multiplied by 100 (this carries the heaviest weight because
                        if all stems were matched then this must be the exact word!) Multiplying by 100 ensures that this weight has the greatest 
                        impact on the final calculation.

                        The second weight is 100 minus the length of the matched word, this is because a search for 'chris' needs to return
                        'chris' before 'christopher','christine','christian' but they would all score the same on the number of stems matched.
                        The second weight is subtracted from 100 to give a 'higher is better' result that is consistent with the first weight...
                        eg 'chris' (100-5=95) should be better than 'christopher' (100-11=89). 100 was chosen because its longer than any word
                        that could be searched and is less than or equal to the multiplier used for the first weight
                        """
                        goodmatches.append((entity_count_dict['entity'], 100*c, 100-len(m)))

        # finally add the two weights together to get an integer and order the results with the highest first
        final = sorted( goodmatches, key=lambda x:x[1] + x[2], reverse=True )

        # convert final matches into proper entity objects
        entities = []
        for result in final:
            e = entity(self.db)
            e._hydrate(result[0])
            entities.append(e)
        
        return entities
        
