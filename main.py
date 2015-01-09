import os
import sys
from Cheetah.Template import Template

HEADER_EXT	= "_HEADER"
HPP_EXT		= ".hpp"
CPP_EXT		= ".cpp"
SRC_FOLDER	= "src"
INC_FOLDER	= "inc"

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

def main():
	className = raw_input('Enter class name: ')

	nameSpace = {'headerName': className.upper() + HEADER_EXT,
			'className': className}
	t = Template(file = sys.path[0] + "/header.tmpl", searchList=[nameSpace])
	createFile(INC_FOLDER, className + HPP_EXT, t)
	t = Template(file = sys.path[0] + "/implementation.tmpl", searchList=[nameSpace])
	createFile(SRC_FOLDER, className + CPP_EXT, t)

main()
