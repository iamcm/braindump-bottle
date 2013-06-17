
from models.BaseModel import BaseModel
import datetime

class Tag(BaseModel):    
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('name', None),
        ('slug', None),
        ('oldId', None),
        ('added', datetime.datetime.now()),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)

    def save(self):
        self.slug = self.name.lower().replace(' ','-')

        BaseModel.save(self)


class Item(BaseModel):
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('title', None),
        ('content', None),
        ('tagIds', []),
        ('oldId', None),
        ('added', datetime.datetime.now()),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)



