import os
import unittest
import datetime
import json

from models.BaseModel import BaseModel
from pymongo import Connection
import settings
from models import Logger

conn = Connection(settings.DBHOST, settings.DBPORT)
_DBCON = conn.test

class ChildModel(BaseModel):
    
    def __init__(self,_DBCON, _id=None):
        
        self.fields = [
            ('title', None),
            ('content', None),
            ('tags', []),
            ('added', datetime.datetime.now()),
        ]
        super(self.__class__, self).__init__(_DBCON, _id) 


class BaseModelTest(unittest.TestCase):

	def setUp(self):
		self._title = 'Jingle Bells'
		self._content = 'Jingle all the way'
		self._tags = ['one', 'two', 3]

	def test_create_child_model(self):
		m = ChildModel(_DBCON)

		self.assertTrue(isinstance(m, ChildModel))


	def test_save_to_database(self):
		m = ChildModel(_DBCON)
		m.save()

		model = _DBCON.ChildModel.find_one()

		self.assertEqual(model['_id'], m._id)

	
	def test_can_fetch_saved_model(self):
		m = ChildModel(_DBCON)
		m.save()

		model = _DBCON.ChildModel.find_one()

		_id = model['_id']
		added = model['added']

		#try and fetch the model
		m = ChildModel(_DBCON, _id)

		self.assertEqual(m._id, _id)
		self.assertEqual(m.added, added)
		

	def test_save_and_update_fields(self):

		_updated_title = 'Bells Jingle'
		_updated_content = 'Yes they do'
		_updated_tags = ['three', 2, 1]

		m = ChildModel(_DBCON)
		m.title = self._title
		m.content = self._content
		m.tags = self._tags
		m.save()

		model = _DBCON.ChildModel.find_one()
		added = model['added']

		#check that the fields all saved correctly
		self.assertEqual(model['_id'], m._id)
		self.assertEqual(model['title'], self._title)
		self.assertEqual(model['content'],self._content)
		self.assertEqual(model['tags'], self._tags)

		#fetch the model
		m = ChildModel(_DBCON, model['_id'])
		m.title = _updated_title
		m.content = _updated_content
		m.tags = _updated_tags
		m.save()

		model = _DBCON.ChildModel.find_one()

		#check that the fields all updates correctly
		self.assertEqual(model['_id'], m._id)
		self.assertEqual(model['title'], _updated_title)
		self.assertEqual(model['content'], _updated_content)
		self.assertEqual(model['tags'], _updated_tags)
		#check that the added field is still the same as when 
		#it was first added
		self.assertEqual(model['added'], added)


	def test_get_hash(self):
		m = ChildModel(_DBCON)
		m.title = self._title
		m.content = self._content
		m.tags = self._tags
		m.save()

		model = _DBCON.ChildModel.find_one()
		m = ChildModel(_DBCON, model['_id'])
		hash = m._get_hash()

		self.assertEqual(model['_id'], hash['_id'])
		self.assertEqual(model['title'], hash['title'])
		self.assertEqual(model['content'], hash['content'])
		self.assertEqual(model['tags'], hash['tags'])
		self.assertEqual(model['added'], hash['added'])
		#_get_hash should create an '__instanceOf__' property so check for that
		self.assertEqual(model['__instanceOf__'], "<class 'basemodel_test.ChildModel'>")


	def test_get_json(self):
		m = ChildModel(_DBCON)
		m.title = self._title
		m.content = self._content
		m.tags = self._tags
		m.save()

		model = _DBCON.ChildModel.find_one()
		m = ChildModel(_DBCON, model['_id'])
		hash = json.loads(m.get_json())

		self.assertEqual(str(model['_id']), hash['_id'])
		self.assertEqual(str(model['title']), hash['title'])
		self.assertEqual(str(model['content']), hash['content'])
		index = 0
		for t in model['tags']:
			self.assertEqual(str(t), eval(hash['tags'])[index])
			index += 1
		self.assertEqual(str(model['added']), hash['added'])


	def tearDown(self):
		#drop the user collection in the test database
		_DBCON.ChildModel.drop()

				

if __name__ == '__main__':
	unittest.main()