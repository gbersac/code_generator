import init
from attributeModel import Attribute

class Class:
	"""docstring for Class"""

	name = ""
	lstAttr = []

	def __init__(self, name):
		self.name = name

	def getGuard(self):
		return self.name.upper() + init.HEADER_EXT

	def addAttr(self, attrType, attrName):
		self.lstAttr.append(Attribute(attrType, attrName))
