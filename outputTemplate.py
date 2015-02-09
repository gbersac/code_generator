import os
import sys
import init
from Cheetah.Template import Template

class OutputTemplate:

	outputImplementation = "header.tmpl"
	outputHeader = "implementation.tmpl"

	def __init__(self, myClass):
		self.cl = myClass


	def process(self):
		nameSpace = {'class': self.cl}
		t = Template(file = self.outputHeader, searchList=[nameSpace])
		self.createFile(init.INC_FOLDER, self.cl.name + init.HPP_EXT, t)
		t = Template(file = self.outputImplementation, searchList=[nameSpace])
		self.createFile(init.SRC_FOLDER, self.cl.name + init.CPP_EXT, t)

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
