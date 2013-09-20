from models.BaseModel import BaseModel
from datetime import datetime

class Category(BaseModel):

	def __init__(self):
		self.name = ''
		self.slug = ''
		self.description = ''
		self.added = None
		self.modified = None
		self.cats = []

	def _presave(self):
		self.slug = self.name.replace(' ','-').lower()
		if not self.added:
			self.added = datetime.now()
		self.modified = datetime.now()