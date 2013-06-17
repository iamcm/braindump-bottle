import os
import unittest
import datetime
import json

from models.BaseModel import BaseModel
from models.EntityManager import EntityManager
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
            ('sort_field', None),
            ('tags', []),
            ('added', datetime.datetime.now()),
        ]
        super(self.__class__, self).__init__(_DBCON, _id) 


class EntityManagerTest(unittest.TestCase):

	def setUp(self):
		for i in range(0,10):
			c = ChildModel(_DBCON)
			c.title = 'Jingle Bells' + str(i)
			c.content = 'Jingle all the way'
			c.sort_field = int(i)
			c.save()

	def test_get_all(self):
		models = EntityManager(_DBCON).get_all(ChildModel)

		#check models is a list
		self.assertTrue(type(models)==list)
		#check we got all ten models
		self.assertTrue(len(models)==10)
		#check that the list contains ChildModel instances
		self.assertTrue(isinstance(models[0], ChildModel))

	def test_filter_criteria_bad_data(self):
		#test for title that doesnt exist
		_title = 'Jingle Bells11'
		models = EntityManager(_DBCON).get_all(ChildModel
												,filter_criteria={'title':_title})
		#check we got no models
		self.assertTrue(len(models)==0)

	def test_filter_criteria_good_data(self):
		#test for title that does exist
		_title = 'Jingle Bells1'
		models = EntityManager(_DBCON).get_all(ChildModel
												,filter_criteria={'title':_title})

		#check we got one model
		self.assertTrue(len(models)==1)
		#confirm its the correct model
		m = models[0]
		self.assertEqual(m.title, _title)

	def test_sort_by(self):
		models = EntityManager(_DBCON).get_all(ChildModel
												,sort_by=[('sort_field', 1)])

		#check the order is correct
		self.assertEqual(models[0].sort_field, 0)
		self.assertEqual(models[9].sort_field, 9)

		#now reverse the order and check again
		models = EntityManager(_DBCON).get_all(ChildModel
												,sort_by=[('sort_field', -1)])

		#check the order is correct
		self.assertEqual(models[0].sort_field, 9)
		self.assertEqual(models[9].sort_field, 0)

	def test_skip(self):
		models = EntityManager(_DBCON).get_all(ChildModel, skip=3)

		#check that we only have 7 models
		self.assertEqual(len(models), 7)
		#check that the first model now is actually the 3rd one created
		self.assertEqual(models[0].sort_field, 3)

	def test_limit(self):
		models = EntityManager(_DBCON).get_all(ChildModel, limit=3)

		#check that we only have 3 models
		self.assertEqual(len(models), 3)
		#check that the first and last models are correct
		self.assertEqual(models[0].sort_field, 0)
		self.assertEqual(models[2].sort_field, 2)

	def test_skip_and_limit(self):
		models = EntityManager(_DBCON).get_all(ChildModel, skip=2, limit=3)

		#check that we only have 3 models
		self.assertEqual(len(models), 3)
		#check that the first and last models are correct
		self.assertEqual(models[0].sort_field, 2)
		self.assertEqual(models[2].sort_field, 4)

	def test_delete_one(self):
		models = EntityManager(_DBCON).get_all(ChildModel)
		m = models[0]

		self.assertEqual(len(models), 10)
		self.assertEqual(models[0].sort_field, 0)

		EntityManager(_DBCON).delete_one('ChildModel', m._id)

		#get the models again and check thet the first in the list is now the second 
		#one that was originally created (as we have just deleted the first one)

		models = EntityManager(_DBCON).get_all(ChildModel)
		self.assertEqual(len(models), 9)
		self.assertEqual(models[0].sort_field, 1)

		



	def tearDown(self):
		#drop the user collection in the test database
		_DBCON.ChildModel.drop()

				

if __name__ == '__main__':
	unittest.main()