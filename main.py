import os
import sys
import init

from classModel import Class
from attributeModel import Attribute
from Cheetah.Template import Template

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

def inputAttrs(myClass):
	print ""
	print myClass.name + ": insert all attributes ('_' will be added)"
	print "Default type is : " +  init.DEFAULT_TYPE
	while True:
		attrName = raw_input('Enter attr name: ')
		if attrName == "":
			return
		attrType = raw_input('Enter attr type: ')
		myClass.addAttr(attrType, attrName)

def main():
	className = raw_input('Enter class name: ')
	myClass = Class(className)
	inputAttrs(myClass)

	nameSpace = {'class': myClass}
	t = Template(file = sys.path[0] + "/header.tmpl", searchList=[nameSpace])
	createFile(init.INC_FOLDER, myClass.name + init.HPP_EXT, t)
	t = Template(file = sys.path[0] + "/implementation.tmpl", searchList=[nameSpace])
	createFile(init.SRC_FOLDER, myClass.name + init.CPP_EXT, t)

main()
