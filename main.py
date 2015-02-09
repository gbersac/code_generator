import os
import sys
import init

from classModel import Class
from attributeModel import Attribute
from outputTemplate import OutputTemplate


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

def inputParent(myClass):
	print ""
	myClass.parentClass = raw_input('Enter parent class name: ')
	print ""

def main():
	className = raw_input('Enter class name: ')
	myClass = Class(className)
	inputParent(myClass)
	inputAttrs(myClass)
	ot = OutputTemplate(myClass)
	ot.process()

main()
