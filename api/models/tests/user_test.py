import os
import unittest
from models.User import User
from pymongo import Connection
import settings
from models import Logger

conn = Connection(settings.DBHOST, settings.DBPORT)
_DBCON = conn.test

class UserTest(unittest.TestCase):

	def setUp(self):
		self.EMAIL = 'an@email.com'
		self.PASSWORD = 'passpass'
		self.TOKEN = None

	def create_user(self):
		u = User(_DBCON)
		u.email = self.EMAIL
		u.password = self.PASSWORD
		u.save()

		return u

	def create_activated_user(self):
		"""
		shortcut to save having to activate the user each time we 
		create one
		"""
		u = User(_DBCON)
		u.email = self.EMAIL
		u.password = self.PASSWORD
		u.valid = True
		u.save()

		return u

	def test_create_user(self):
		u = self.create_user()

		self.TOKEN = u.token

		self.assertTrue(self.TOKEN is not None)
		self.assertTrue(u._id is not None)

	def test_get_user_bad(self):
		self.create_user()

		u = User(_DBCON, email=self.EMAIL, password='invalid')

		self.assertTrue(u._id is None)

	def test_get_user_good_but_user_not_valid(self):
		self.create_user()

		u = User(_DBCON, email=self.EMAIL, password=self.PASSWORD)

		self.assertTrue(u._id is None)
		self.assertFalse(u.valid)
	
	def test_activate_user_bad_token(self):
		self.create_user()

		u = User(_DBCON)
		self.assertFalse(u.activate('asdf'))

	def test_activate_user_good_token(self):
		self.create_user()

		user = _DBCON.User.find_one()

		u = User(_DBCON)
		self.assertTrue(u.activate(user['token']))
		self.assertTrue(u.valid)
		self.assertTrue(u.email == self.EMAIL)

	def test_get_user_good_after_activation(self):
		self.create_activated_user()

		u = User(_DBCON, email=self.EMAIL, password=self.PASSWORD)

		self.assertTrue(u._id is not None)

	def test_password_is_still_the_same_after_user_instance_being_saved(self):
		u = self.create_activated_user()

		u = User(_DBCON, email=self.EMAIL, password=self.PASSWORD)
		u.save()

		#now try and get that user again with the same email and password
		u = User(_DBCON, email=self.EMAIL, password=self.PASSWORD)

		self.assertTrue(u._id is not None)

	def test_change_password_bad(self):
		u = self.create_activated_user()

		u = User(_DBCON, email=self.EMAIL, password=self.PASSWORD)
		u.password = 'new'
		u.save()

		#now try and get that user again with the new email and password
		u = User(_DBCON, email=self.EMAIL, password='new')

		self.assertTrue(u._id is None)

	def test_change_password_good(self):
		u = self.create_activated_user()

		u = User(_DBCON, email=self.EMAIL, password=self.PASSWORD)
		u.password = 'new'
		u.save(True)

		#now try and get that user again with the new email and password
		u = User(_DBCON, email=self.EMAIL, password='new')

		self.assertTrue(u._id is not None)


	def tearDown(self):
		#drop the user collection in the test database
		os.system('mongo test --eval "db.User.drop()" > /dev/null')

				

if __name__ == '__main__':
	unittest.main()