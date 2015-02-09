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

	def initList(self):
		initStrs = []
		for att in self.lstAttr:
			initStr = att.getName() + "(" + att.defaultValue() + ")"
			if att.defaultValue() != "" or att.isConst:
				initStrs.append(initStr)
		return ", ".join(initStrs)

	def initCopyList(self):
		initStrs = []
		for att in self.lstAttr:
			if att.isConst:
				initStr = att.getName() + "(model." + att.getName() + ")"
				initStrs.append(initStr)
		return ", ".join(initStrs)
