import os, sys
sys.path.append(os.path.abspath( os.path.join(__file__,'../../..')))

import os
import unittest
from models.Models import Tag
from pymongo import Connection
import settings
from models import Logger

conn = Connection(settings.DBHOST, settings.DBPORT)
_DBCON = conn.test

class UserTest(unittest.TestCase):

    def setUp(self):
        pass

    def create_tag(self):
        t = Tag(_DBCON)
        t.name = 'Tag 1'
        t.save()

        return t

    def test_create_tag(self):
        t = self.create_tag()

        self.assertTrue(t._id is not None)

    def test_slug(self):
        t = self.create_tag()

        self.assertTrue(t.slug == 'tag-1')

    def tearDown(self):
        #drop the user collection in the test database
        os.system('mongo test --eval "db.Tag.drop()" > /dev/null')

                

if __name__ == '__main__':
    unittest.main()