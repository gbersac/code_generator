import os
import sys
from Cheetah.Template import Template

HEADER_EXT		= "_HEADER"
HPP_EXT			= ".hpp"
CPP_EXT			= ".cpp"
SRC_FOLDER		= "src"
INC_FOLDER		= "inc"
DEFAULT_TYPE	= "std::string"

class Attribute:
	"""docstring for Attribute"""

	aType = DEFAULT_TYPE
	name = "name"

	def __init__(self, _aType, _name):
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


def createFile(targetFolder, fileName, content):
	if os.path.exists(targetFolder):
		fileName = targetFolder + "/" + fileName
	#check is the file exist
	if os.path.exists(fileName):
		print "The file " + fileName + " already exist. Nothing done."
		return
	#insert the content in the file
	f = open(fileName, "a")
	f.write(str(content))
	f.close()
	print fileName + " created"

def inputAttrs(className):
	print ""
	print className + ": insert all attributes ('_' will be added)"
	print "Default type is : " +  DEFAULT_TYPE
	lstAttr = []
	while True:
		attrName = raw_input('Enter attr name: ')
		if attrName == "":
			return lstAttr
		attrType = raw_input('Enter attr type: ')
		if attrType == "":
			attrType = DEFAULT_TYPE
		lstAttr.append(Attribute(attrType, attrName))


def main():
	className = raw_input('Enter class name: ')
	lstAttr = inputAttrs(className)

	nameSpace = {'headerName': className.upper() + HEADER_EXT,
			'className': className,
			'lstAttr': lstAttr}
	t = Template(file = sys.path[0] + "/header.tmpl", searchList=[nameSpace])
	createFile(INC_FOLDER, className + HPP_EXT, t)
	t = Template(file = sys.path[0] + "/implementation.tmpl", searchList=[nameSpace])
	createFile(SRC_FOLDER, className + CPP_EXT, t)

main()
