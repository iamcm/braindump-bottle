import os, sys
sys.path.append(os.path.abspath( os.path.join(__file__,'../../..')))

import os
import unittest
from models.Models import Item
from pymongo import Connection
import settings
from models import Logger

conn = Connection(settings.DBHOST, settings.DBPORT)
_DBCON = conn.test

class UserTest(unittest.TestCase):

    def setUp(self):
        pass

    def create_item(self):
        i = Item(_DBCON)
        i.title = 'the title'
        i.content = 'the content'
        i.tagIds = [1,2,3]
        i.save()

        return i

    def test_create_item(self):
        i = self.create_item()

        self.assertTrue(i._id is not None)

    def tearDown(self):
        #drop the user collection in the test database
        os.system('mongo test --eval "db.Item.drop()" > /dev/null')

                

if __name__ == '__main__':
    unittest.main()