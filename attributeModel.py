import init

class Attribute:
	"""docstring for Attribute"""

	aType = init.DEFAULT_TYPE
	name = "name"

	def __init__(self, _aType, _name):
		if _aType == "":
			self.aType = init.DEFAULT_TYPE
		else:
			self.aType = _aType
		self.name = _name

	def getName(self):
		return "_" + self.name

	def getGetterName(self):
		return "get" + self.name[0].upper() + self.name[1:]

	def getSetterName(self):
		return "set" + self.name[0].upper() + self.name[1:]

	def __str__(self):
	     return "{" + self.aType + ", " + self.name + "}"
