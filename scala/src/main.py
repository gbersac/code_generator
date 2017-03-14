#! /usr/local/bin/python
import os
import sys
import argparse

from Cheetah.Template import Template

class FieldType:
	CLASS = 1
	STRING = 2
	DATE = 3

class Field:
	"""Dic is a dictionnary of field name and their filds"""
	def __init__(self, name, definition, level = 0):
		self.name = name
		self.level = level
		if isinstance(definition, dict):
			self.type = FieldType.CLASS
			self.childs = []
			for k, v in definition.items():
				child = Field(k, v, level + 1)
				self.childs.append(child)
		elif isinstance(definition, list):
			if name.find("date") != -1:
				self.type = FieldType.DATE
			else:
				self.type = FieldType.STRING
			self.path = definition
		else:
			print("!!! Error for", name, "the definition is neither a list neither a dictionary.")
			sys.exit()

	def preIndent(self):
		return '  ' * self.level

	def __str__(self):
		if self.type == FieldType.CLASS:
			childsStr = list(map(lambda x: x.__str__(), self.childs))
			return self.preIndent() + self.name + ' ->\n' + "\n".join(childsStr)
		elif self.type == FieldType.STRING:
			return self.preIndent() + self.name
		elif self.type == FieldType.DATE:
			return self.preIndent() + self.name + '[date]'
		else:
			return 'unknown type'

	def typeName(self):
		if self.type == FieldType.STRING:
			return 'String'
		elif self.type == FieldType.DATE:
			return 'DateTime'
		elif self.type == FieldType.CLASS:
			name = self.name[0].upper() + self.name[1:]
			return name

	def xmlPath(self):
		if self.type == FieldType.CLASS:
			path = []
			for child in self.childs:
				if child.type != FieldType.CLASS:
					return child.path[0: -1]
			print("!!! error cannot find path for " + self.name)
		else:
			return self.path

	def xmlValidator(self):
		path = list(map(lambda x: '"' + x + '"', self.xmlPath()))
		strPath = " \ ".join(path)
		return '      (__ \ "root" \ {0}).read[{1}]'.format(strPath, self.typeName())

	############################################################################
	######################### specific to class types ##########################

	def classChildren(self):
		childs = []
		for child in self.childs:
			if child.type == FieldType.CLASS:
				childs.append(child)
		return childs

	def toScalaCaseClass(self):
		t = Template(file = 'case_class.tmpl', searchList=[{'class': self}])
		lines = str(t).split('\n')
		def toInnerClass(field):
			toString = field.toScalaCaseClass()
			lines = toString.split('\n')
			return '\n'.join(map(lambda x: self.preIndent() + x, lines))
		classChildren = list(map(toInnerClass, self.classChildren()))
		return str(t) + "\n\n".join(classChildren) + '\n}'


	def attributeList(self):
		def childType(child):
			if child.type == FieldType.CLASS:
				return child.name + ': ' + self.typeName() + '.' + child.typeName()
			else:
				return child.name + ': ' + child.typeName()
		childsTypes = list(map(childType, self.childs))
		if self.childs <= 3:
			return ', '.join(childsTypes)
		else:
			return '\n  ' + ',\n  '.join(childsTypes) + '\n'

	def childsXmlValidator(self):
		validators = list(map(lambda x: x.xmlValidator(), self.childs))
		return " ~\n".join(validators)

"""
root is an array of string which refered to the beginning of each lines to discard
"""
def groupsLines(lines, root = []):
	result = {}
	for line in lines:
		attributeName = line[len(root)]
		if attributeName in result:
			result[attributeName].append(line)
		else:
			result[attributeName] = [line]
	for k, v in result.items():
		if len(v) > 1:
			newRoot = list(root)
			newRoot.append(k)
			result[k] = groupsLines(v, newRoot)
		else:
			result[k] = v[0]
	return result

def createFile(fileName, content):
	#check if the file exist
	if os.path.exists(fileName):
		print("The file " + fileName + " already exist. Nothing done.")
		return
	#insert the content in the file
	f = open(fileName, "a")
	f.write(str(content))
	f.close()

def parseLines(lines):
	lines = list(map(lambda x: x.split(), lines))
	rootDefinition = groupsLines(lines)
	# for k, v in result.items():
	# 	print(k, " ->", v)
	root = Field('root', rootDefinition)
	print(root)
	t = Template(file = 'main_file.tmpl', searchList=[{'class': root}])
	createFile('OMContrat.scala', t)

def main():
	if len(sys.argv) != 2:
		print("Error input file as argument required.")
	inputFile = sys.argv[1]
	file = open(inputFile, 'r')
	lines = file.readlines()
	classes = parseLines(lines)

main()
