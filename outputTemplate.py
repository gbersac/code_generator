import os
import sys
import init
from Cheetah.Template import Template

class OutputTemplate:
	"""docstring for outputTemplate"""
	def __init__(self, myClass):
		nameSpace = {'class': myClass}
		t = Template(file = sys.path[0] + "/header.tmpl", searchList=[nameSpace])
		self.createFile(init.INC_FOLDER, myClass.name + init.HPP_EXT, t)
		t = Template(file = sys.path[0] + "/implementation.tmpl", searchList=[nameSpace])
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



