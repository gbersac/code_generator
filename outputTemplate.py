import os
import sys
import init
from Cheetah.Template import Template

class OutputTemplate:
	cl
	outputImplementation
	outputHeader

	"""docstring for outputTemplate"""
	def pathTemplate(self, tmplName):
		modpath = __file__
		modpath = modpath[:-1]
		print "###" + os.path.abspath(__file__)
		print "###" + os.path.split(os.path.abspath(__file__))[0]
		dirName = os.path.split(os.path.abspath(__file__))[0]
		outputImplementation = dirName + "header.tmpl"
		outputHeader = dirName + "implementation.tmpl"
		return  + "/" + tmplName

	def __init__(self, myClass):
		cl = myClass

		nameSpace = {'class': myClass}
		t = Template(file = outputHeader, searchList=[nameSpace])
		self.createFile(init.INC_FOLDER, myClass.name + init.HPP_EXT, t)
		t = Template(file = outputImplementation, searchList=[nameSpace])
		self.createFile(init.SRC_FOLDER, myClass.name + init.CPP_EXT, t)

	def createFile(slef, targetFolder, fileName, content):
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
