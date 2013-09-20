from pymongo import MongoClient
from bson.objectid import ObjectId
import models
from settings import DBHOST, DBPORT, DBNAME

class EntityManager:

    def __init__(self, db=None):
        client = MongoClient(DBHOST, port=DBPORT)
        self.db = client[db or DBNAME]
        

    def _hydate(self, data):
        """
        Use the given data to identify and populate and instance an entity
        """
        entity = self._unicode_to_class_instance(data.get('__instanceOf__'))
        setattr(entity, '_id', data.get('_id'))

        #for each property in this entity class
        for prop in dir(entity):
            #we dont want anything callable e.g. methods, __doc__, etc
            if not callable(getattr(entity, prop)) and not prop.startswith('__'):
                #get this property's type
                proptype = type(getattr(entity, prop))
                #get the value from the data for this property
                propvalue = data.get(prop)

                #if this is a list then iterate each list item and
                #hydrate any entities if necessary
                if proptype == list:
                    items = []
                    for item in propvalue:
                        #we can tell if this is an entity that we need to hydrate by
                        #looking for dict's with our signature __instanceOf__ item
                        if type(item)==dict and item.has_key('__instanceOf__'):
                            #hydrate this item
                            entityinstance = self._unicode_to_class_name(item['__instanceOf__'])
                            entityid = item['_id']

                            #add this item to the list of hydrated items
                            item = self.find_one(entityinstance, entityid)

                        items.append(item)

                    #set this property value to be the list of processed items
                    propvalue = items

                #else if this is a dict that we need to hydrate
                elif type(propvalue)==dict and propvalue.has_key('__instanceOf__'):
                    #hydrate this item
                    entityinstance = self._unicode_to_class_name(propvalue['__instanceOf__'])
                    entityid = propvalue['_id']

                    propvalue = self.find_one(entityinstance, entityid)

                #now assign our final propvalue to our entity
                setattr(entity, prop, propvalue)

        return entity


    def _entity_to_dict(self, entity, saveChildEntities=False):
        """
        Convert an entity class to a dict in order to persist it to the database
        Note we cant just call entity.__dict__ because we want to find any entity 
        instances inside this class, eg User.groups = [<GroupInstance>, <GroupInstance>]
        and convert these as well.
        saveChildEntities determines whether or not to automatically save any child entities 
        found inside this class, it is always True when called from this classes save method
        but False by default to allow for this method to be called in a debugging context so that
        nothing gets written to the database
        """
        obj = {}
        #for each property in this entity class
        for prop in dir(entity):
            #we dont want anything callable e.g. methods, __doc__, etc
            if not callable(getattr(entity, prop)) and not prop.startswith('__'):
                #get this property's type
                proptype = type(getattr(entity, prop))
                #get the value from the data for this property
                propvalue = getattr(entity, prop)

                #eg User.groups = [<GroupEntity>,<GroupEntity>,<GroupEntity>]
                if proptype == list:
                    items = []

                    for item in propvalue:
                        #if the items in this list are entities then convert them to an object as well
                        if hasattr(item, '_presave') and saveChildEntities:
                            #save the entity
                            id = self.save(self._unicode_to_class_name(str(entity.__class__)), item)
                            #get it in its fully populated state
                            item = self.find_one(self._unicode_to_class_name(str(entity.__class__)), id)
                            #convert this entity
                            item = self._entity_to_dict(item)
                        
                        #add this item to the list of processed items
                        items.append(item)

                    #set this property value to be the list of processed items
                    propvalue = items

                #eg User.role = <UserRoleEntity>
                elif hasattr(propvalue, '_presave') and saveChildEntities:
                    #save the entity
                    id = self.save(self._unicode_to_class_name(str(entity.__class__)), propvalue)
                    #get it in its fully populated state
                    propvalue = self.find_one(self._unicode_to_class_name(str(entity.__class__)), id)
                    #convert this entity
                    propvalue = self._entity_to_dict(propvalue)

                obj[prop] = propvalue


        # add __class__ as metadata with the name of __instanceOf__ so we can grab it when
        # hydrating an entity
        obj['__instanceOf__'] = str(entity.__class__)
        
        return obj


    
    def _unicode_to_class_instance(self, string):
        """
        Takes the output of <class>.__class__ and returns an instance of that class

        eg:
        Item.__class__ returns:
            <class 'models.Item.Item'>
        so calling _unicode_to_class_instance on this would return an instance of: 
            models.Item.Item
        """
        return eval(string[string.find("'")+1:string.rfind("'")]+'()')


    def _unicode_to_class_name(self, string):
        """
        Takes the output of <class>.__class__ and returns a string describing that class
        without its namespace 

        eg:
        Item.__class__ returns:
            <class 'models.Item.Item'>
        so calling _unicode_to_class_name on this would return: 
            'Item'
        which can be used to call other methods on this class:
            self.find_one('Item', '<itemid>')
        """
        return str(string[string.rfind(".")+1:string.rfind("'")])


    def find_raw(self, collectionname):
        """
        Find all entries for a given collection
        """
        return self.db[collectionname].find()


    def find(self, collectionname):
        """
        Find all entries for a given collection and return them as a instances of the given entity
        """
        items = []
        for item in self.find_raw(collectionname):
            items.append(self._hydate(item))

        return items


    def find_one_raw(self, collectionname, id):
        """
        Find one for a given collection
        """
        return self.db[collectionname].find_one({'_id':ObjectId(id)})


    def find_one(self, collectionname, id):
        """
        Find one for a given collection and return it as an instance of the given entity
        """
        item = self.find_one_raw(collectionname, id)
        if item:
            item = self._hydate(item)
        return item


    def save(self, collectionname,  entity):
        """
        Insert or Update a single entity and return the _id of the saved entity
        """
        #call the pre-save hook
        entity._presave()

        obj = self._entity_to_dict(entity, True)
        
        return self.db[collectionname].save(obj)


    def remove_one(self, collectionname, id):
        """
        Delete one entity by id
        """
        self.db[collectionname].remove({'_id':ObjectId(id)})

