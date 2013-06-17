import random
import json
import datetime
import os 
import bottle
import settings
import re
from bson import ObjectId
from db import _DBCON
from models import Util
from models.EntityManager import EntityManager
from models.Session import Session
from models.Email import Email
from models import Logger
from models.User import User
from models.Models import Tag, Item



def checklogin(callback):
    def wrapper(*args, **kwargs):
        if bottle.request.get_cookie('token') or bottle.request.GET.get('token'):
            token = bottle.request.get_cookie('token') or bottle.request.GET.get('token')
            
            s = Session(_DBCON, publicId=token)
            if not s.valid or not s.check(bottle.request.get('REMOTE_ADDR'), bottle.request.get('HTTP_USER_AGENT')):
                return bottle.HTTPError(403, 'Access denied')
                
            else:
                bottle.request.session = s
                return callback(*args, **kwargs)
        else:
            return bottle.HTTPError(403, 'Access denied')
    return wrapper


def JSONResponse(callback):
    def wrapper(*args, **kwargs):
        bottle.response.content_type = 'text/json'
        return callback(*args, **kwargs)
    return wrapper


# static files
if settings.PROVIDE_STATIC_FILES:
    @bottle.route('/<filepath:path>')
    def index(filepath):
        return bottle.static_file(filepath, root=settings.ROOTPATH +'/../frontend/')




# auth
def loginUser(userId):
    s = Session(_DBCON)
    s.userId = userId
    s.ip = bottle.request.get('REMOTE_ADDR')
    s.userAgent = bottle.request.get('HTTP_USER_AGENT')
    s.save()

    return s.publicId


@bottle.route('/api/login', method='POST')
@JSONResponse
def index():
    e = bottle.request.POST.get('email')
    p = bottle.request.POST.get('password')

    if e and p:
        u = User(_DBCON, email=e, password=p)

        if u._id and u.valid:
            loginUser(u._id)

            output = {'success':1}
        else:
            output = {
                'success':0,
                'error':'Login failed'
            }
    else:
        output = {
            'success':0,
            'error':'Login failed'
        }

    return json.dumps(output)



@bottle.route('/api/logout', method='GET')
@checklogin
def index():
    s = bottle.request.session
    s.destroy()
    
    return ''





#######################################################
# Main app routes
#######################################################
@bottle.route('/api/tags')
@checklogin
@JSONResponse
def index():
    output = []
    for t in EntityManager(_DBCON).get_all(Tag, sort_by=[('name',1)]):
        output.append(t.get_json_safe())

    return json.dumps(output)



@bottle.route('/api/tag', method='POST')
@checklogin
@JSONResponse
def index():
    n = bottle.request.POST.get('name')

    if n:
        t = Tag(_DBCON)
        t.name = n
        t.save()

        return ''
        
    else:
        return bottle.HTTPError(400)



@bottle.route('/api/tag/:id', method='GET')
@checklogin
@JSONResponse
def index(id):
    t = Tag(_DBCON, _id=id)

    return json.dumps(t.get_json_safe())


@bottle.route('/api/tag/:id', method='POST')
@checklogin
@JSONResponse
def index(id):
    n = bottle.request.POST.get('name')

    if n:
        try:
            t = Tag(_DBCON, _id=id)
        except:
            return bottle.HTTPError(404)
        t.name = n
        t.save()

        return ''
        
    else:
        return bottle.HTTPError(400)



@bottle.route('/api/tag/:id/delete', method='POST')
@checklogin
@JSONResponse
def index(id):
    try:
        t = Tag(_DBCON, _id=id)
    except:
        return bottle.HTTPError(404)

    EntityManager(_DBCON).delete_one('Tag', t._id)

    return ''



@bottle.route('/api/items')
@checklogin
@JSONResponse
def index():
    tag = bottle.request.GET.get('tag','all')


    if tag != 'all':
        tags = EntityManager(_DBCON).get_all(Tag, filter_criteria={'slug':tag})
        if tags:
            tag = tags[0]
        else:
            return bottle.HTTPError(404)

        filter_criteria = {
            'tagIds':{
                '$in':[str(tag._id)]
            }
        }
    else:
        filter_criteria = {}


    output = []
    for i in EntityManager(_DBCON).get_all(Item, filter_criteria=filter_criteria, sort_by=[('added',-1)]):
        output.append(i.get_json_safe())

    return json.dumps(output)



@bottle.route('/api/item', method='POST')
@checklogin
@JSONResponse
def index():
    t = bottle.request.POST.get('title')
    c = bottle.request.POST.get('content')
    tagIds = bottle.request.POST.getall('tagIds[]')

    if t and c and tagIds:
        i = Item(_DBCON)
        i.title = t
        i.content = c
        i.tagIds = []
        for tagId in tagIds:
            i.tagIds.append(tagId)

        if bottle.request.POST.get('tag'):
            newtag = Tag(_DBCON)
            newtag.name = bottle.request.POST.get('tag')
            newtag.save()
            
            i.tagIds.append(newtag._id)

        i.save()
        
        return ''
        
    else:
        return bottle.HTTPError(400)



@bottle.route('/api/item/:id', method='GET')
@checklogin
@JSONResponse
def index(id):
    i = Item(_DBCON, _id=id)

    return json.dumps(i.get_json_safe())


@bottle.route('/api/item/:id', method='POST')
@checklogin
@JSONResponse
def index(id):
    t = bottle.request.POST.get('title')
    c = bottle.request.POST.get('content')
    tagIds = bottle.request.POST.getall('tagIds[]')

    if t and c and tagIds:
        try:
            i = Item(_DBCON, _id=id)
        except:
            return bottle.HTTPError(404)

        i.title = t
        i.content = c
        i.tagIds = []
        for tagId in tagIds:
            i.tagIds.append(tagId)

        if bottle.request.POST.get('tag'):
            newtag = Tag(_DBCON)
            newtag.name = bottle.request.POST.get('tag')
            newtag.save()
            
            i.tagIds.append(newtag._id)

        i.save()
        
        return ''
        
    else:
        return bottle.HTTPError(400)



@bottle.route('/api/item/:id/delete', method='POST')
@checklogin
@JSONResponse
def index(id):
    try:
        i = Item(_DBCON, _id=id)
    except:
        return bottle.HTTPError(404)

    EntityManager(_DBCON).delete_one('Item', i._id)

    return ''




@bottle.route('/api/search/:searchterm')
@checklogin
@JSONResponse
def index(searchterm):
    output = []

    items1 = EntityManager(_DBCON).get_all(Item, filter_criteria={
                                                    '$or':[
                                                        {'title':{'$regex':searchterm, '$options': 'i' }},
                                                        {'content':{'$regex':searchterm, '$options': 'i' }},
                                                    ]})

    if not items1:
        items1 = []

    tags = [str(t._id) for t in EntityManager(_DBCON).get_all(Tag, filter_criteria={'name':{'$regex':searchterm, '$options': 'i' }})]

    items2 = []
    if len(tags)>0:
        items2 = EntityManager(_DBCON).get_all(Item, filter_criteria={
                                                'tagIds':{
                                                    '$in':tags
                                                }
                                            })


    items1.extend(items2)    

    for i in items1:
        output.append(i.get_json_safe())

    return json.dumps(output)





#######################################################

if __name__ == '__main__':
    with open(settings.ROOTPATH +'/app.pid','w') as f:
        f.write(str(os.getpid()))

    if settings.DEBUG: 
        bottle.debug() 
        
    bottle.run(server=settings.SERVER, reloader=settings.DEBUG, host=settings.APPHOST, port=settings.APPPORT, quiet=(settings.DEBUG==False) )
