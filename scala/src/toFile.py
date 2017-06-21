import os

from Cheetah.Template import Template

outputFolder = 'output'

def createFile(fileName, content):
	path = outputFolder + '/' + fileName[0].upper() + fileName[1:] + '.scala'
	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
	#check if the file exist
	if os.path.exists(path):
		print("The file " + fileName + " already exist. Nothing done.")
		return
	#insert the content in the file
	f = open(path, "a")
	f.write(str(content))
	f.close()

def toFile(field):
	fileName = field.className()
	t = Template(file = 'main_file.tmpl', searchList=[{'class': field}])
	createFile(fileName, t)

def toRootFile(field):
	fileName = field.className()
	t = Template(file = 'main_file.tmpl', searchList=[{'class': field}])
	createFile(fileName, t)
