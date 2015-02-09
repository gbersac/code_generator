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

	aType	= init.DEFAULT_TYPE
	name	= "name"
	isConst	= False
	ptrType	= PointerType.NONE
	nbPtr	= 0

	def __init__(self, _aType, _name):
		self.setType(_aType)
		self.name = _name

	def setType(self, strg):
		if str == "":
			self.aType = init.DEFAULT_TYPE
			return
		if re.match(expandRegex(regexConst), strg):
			self.isConst = True
			strg = re.sub("const", "", strg)
		if re.match(expandRegex(regexPointer), strg):
			self.nbPtr = len(re.findall(regexPointer, strg))
			self.ptrType = PointerType.POINTER
			strg = re.sub(regexPointer, "", strg)
		if re.match(expandRegex(regexReference), strg):
			self.ptrType = PointerType.REFERENCE
			strg = re.sub(regexReference, "", strg)
		self.aType = strg.strip()

	def getName(self):
		return "_" + self.name

	def expandPrt(self):
		return ''.join(['*' for s in xrange(self.nbPtr)])

	def getType(self):
		print "ptrType: " + str(self.ptrType) + " isConst: " + str(self.isConst)
		if self.ptrType == PointerType.POINTER:
			if self.isConst:
				return self.aType + " const" + self.expandPrt()
			return self.aType + self.expandPrt()
		if self.ptrType == PointerType.REFERENCE:
			return self.aType + "&"
		if self.isConst:
			return self.aType + " const"
		return self.aType

	def getGetterName(self):
		return "get" + self.name[0].upper() + self.name[1:]

	def getSetterName(self):
		return "set" + self.name[0].upper() + self.name[1:]

	def getGetterRetType(self):
		if self.ptrType == PointerType.POINTER:
			if self.isConst:
				return self.aType + " const" + self.expandPrt()
			return self.aType + self.expandPrt()
		return self.aType + " const&"

	def getSetterArgType(self):
		if self.ptrType == PointerType.POINTER:
			if self.isConst:
				return self.aType + " const" + self.expandPrt()
			return self.aType + self.expandPrt()
		return self.aType + " const&"

	"""Return a string defining the default value of the attribute"""
	def defaultValue(self):
		if self.aType in ["int", "long", "unsigned", "short"]:
			return "0"
		if self.aType in ["float", "double"]:
			return "0.0"
		if self.aType in ["char"]:
			return "\\0"
		if self.aType in ["std::string", "string"]:
			return "\"\""
		return ""

	def __str__(self):
	     return "{" + self.aType + ", " + self.name + "}"
