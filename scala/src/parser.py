"""
The purpose of this file is to take a line from the input file and transform
it to a `Field` class.
"""

import copy

from field import FieldType, Field

class CSVLine:
	def __init__(self, tokens):
		self.code1 = tokens[0]
		self.libelle1 = tokens[1]
		self.code2 = tokens[2]
		self.libelle2 = tokens[3]
		self.code3 = tokens[4]
		self.libelle3 = tokens[5]
		self.code4 = tokens[6]
		self.libelle4 = tokens[7]
		self.code5 = tokens[8]
		self.libelle5 = tokens[9]
		self.code6 = tokens[10]
		self.libelle6 = tokens[11]
		if tokens[12] == 'N':
			self.isMandatory = False
		else:
			self.isMandatory = True
		self.format = tokens[13]
		self.lineType = tokens[14]
		self.codification = tokens[15]
		self.commentaire = tokens[16]

	def path(self):
		codes = [self.code1, self.code2, self.code3, self.code4, self.code5, self.code6]
		toReturn = []
		for el in codes:
			if el != '':
				toReturn.append(el)
		return codes

	def name(self):
		return self.firstCode().partition('(')[0]

	def firstCode(self):
		if self.code1 != '':
			return self.code1
		elif self.code2 != '':
			return self.code2
		elif self.code3 != '':
			return self.code3
		elif self.code4 != '':
			return self.code4
		elif self.code5 != '':
			return self.code5
		elif self.code6 != '':
			return self.code6

	def libelle(self):
		if self.code1 != '':
			return self.libelle1
		elif self.code2 != '':
			return self.libelle2
		elif self.code3 != '':
			return self.libelle3
		elif self.code4 != '':
			return self.libelle4
		elif self.code5 != '':
			return self.libelle5
		elif self.code6 != '':
			return self.libelle6

	def level(self):
		if self.code1 != '':
			return 1
		elif self.code2 != '':
			return 2
		elif self.code3 != '':
			return 3
		elif self.code4 != '':
			return 4
		elif self.code5 != '':
			return 5
		elif self.code6 != '':
			return 6

	def nextLevel(self):
		if self.code1 != '':
			return 2
		elif self.code2 != '':
			return 3
		elif self.code3 != '':
			return 4
		elif self.code4 != '':
			return 5
		elif self.code5 != '':
			return 6

	def hasFieldInSameLine(self):
		if self.code1 != '':
			return self.code2 == ''
		elif self.code2 != '':
			return self.code3 == ''
		elif self.code3 != '':
			return self.code4 == ''
		elif self.code4 != '':
			return self.code5 == ''
		elif self.code5 != '':
			return self.code6 == ''
		return False

	def isObject(self):
		return self.fieldType() == FieldType.CLASSUNIQUE or self.fieldType() == FieldType.CLASSLIST

	def delCodeByNumber(self, i):
		if i == 1:
			self.code1 = ''
			self.libelle1 = ''
		elif i == 2:
			self.code2 = ''
			self.libelle2 = ''
		elif i == 3:
			self.code3 = ''
			self.libelle3 = ''
		elif i == 4:
			self.code4 = ''
			self.libelle4 = ''
		elif i == 5:
			self.code5 = ''
			self.libelle5 = ''
		elif i == 6:
			self.code6 = ''
			self.libelle6 = ''

	def fieldType(self):
		if '(unique)' in self.firstCode():
			return FieldType.CLASSUNIQUE
		elif '(liste)' in self.firstCode():
			return FieldType.CLASSLIST
		elif self.firstCode().startswith('flag'):
			return FieldType.YESNO
		elif 'date' in self.firstCode() or self.lineType == 'DATE':
			return FieldType.DATE
		elif 'NUMBER' in self.lineType:
			return FieldType.DOUBLE
		else:
			return FieldType.STRING

"""
Sometime, there is more than one child on the same line
"""
def getSameLineChild(obj):
	child = copy.copy(obj)
	child.delCodeByNumber(obj.level())
	return child

"""
lines: the first line is the one to transform to a Fields.
	Other lines maybe the childs of that first one.
"""
def toField(lines):
	toTransform = lines[0]
	if toTransform.isObject():
		childs = [] # list of Field
		lines = [getSameLineChild(toTransform)] + lines[1:]
		for i in range(len(lines)):
			child = lines[i]
			if child.level() == toTransform.level() + 1:
				childs.append(toField(lines[i:]))
			elif child.level() <= toTransform.level():
				break
		return Field(toTransform.name(), toTransform.fieldType(),
			toTransform.libelle(), toTransform.isMandatory, toTransform.level(),
			childs)
	else:
		return Field(toTransform.name(), toTransform.fieldType(),
			toTransform.libelle(), toTransform.isMandatory, toTransform.level())

def parse(inputLines):
	lines = []
	for line in inputLines:
		lines.append(CSVLine(line))
	fields = []
	for i in range(len(lines)):
		obj = lines[i]
		if obj.level() == 1:
			fields.append(toField(lines[i:]))
	return fields
