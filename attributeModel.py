import init
import re

regexConst		= "(^|[^a-zA-Z])const([^a-zA-Z]|$)"
regexPointer	= "\\*"
regexReference	= "&"

class PointerType:
	NONE = 1
	POINTER = 2
	REFERENCE = 3

def expandRegex(strg):
	return ".*" + strg + ".*"

class Attribute:
	"""docstring for Attribute"""

	aType = init.DEFAULT_TYPE
	name = "name"
	isConst = False
	ptrType = PointerType.NONE

	def __init__(self, _aType, _name):
		self.setType(_aType)
		self.name = _name

	def setType(self, strg):
		if str == "":
			self.aType = init.DEFAULT_TYPE
			return
		if re.match(expandRegex(regexConst), strg):
			print "###constant"
			self.isConst = True
			strg = re.sub(regexConst, "", strg)
		if re.match(expandRegex(regexPointer), strg):
			print "###ptr"
			self.ptrType = PointerType.POINTER
			strg = re.sub(regexPointer, "", strg)
		if re.match(expandRegex(regexReference), strg):
			print "###ref"
			self.ptrType = PointerType.REFERENCE
			strg = re.sub(regexReference, "", strg)
		print "result: " + strg
		self.aType = strg.strip()

	def getName(self):
		return "_" + self.name

	def getGetterName(self):
		return "get" + self.name[0].upper() + self.name[1:]

	def getSetterName(self):
		return "set" + self.name[0].upper() + self.name[1:]

	def __str__(self):
	     return "{" + self.aType + ", " + self.name + "}"
