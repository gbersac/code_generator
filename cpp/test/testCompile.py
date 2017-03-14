import unittest
import os
import shutil
import subprocess
import shlex
import src.init

from src.attributeModel import Attribute, PointerType
from src.classModel import Class
from src.outputTemplate import OutputTemplate

TEST_DIR = "test_dir"
CMD_LINE = "g++ -Wall -Wextra -Werror -c "

class TestCompileFunctions(unittest.TestCase):

	def setUp(self):
		self.testNum = 0
		if not os.path.exists(TEST_DIR):
			os.makedirs(TEST_DIR)
		os.chdir(TEST_DIR)
		self.headerPath = "../src/" + "header.tmpl"
		self.implPath = "../src/" + "implementation.tmpl" 

	def tearDown(self):
		os.chdir("..")
		shutil.rmtree(TEST_DIR)

	def isCompiling(self, cl):
		ot = OutputTemplate(cl)
		ot.outputImplementation = self.implPath
		ot.outputHeader = self.headerPath
		ot.process()
		cmd = shlex.split(CMD_LINE + cl.name + src.init.CPP_EXT)
		self.assertEqual(subprocess.call(cmd), 0)

	def basicClass(self, typeAttr, nameAttr):
		cl = Class("Aaa" + str(self.testNum))
		self.testNum += 1
		if nameAttr != "":
			cl.addAttr(typeAttr, nameAttr)
		return cl

	def basicChildClass(self, typeAttr, nameAttr):
		cl = self.basicClass(typeAttr, nameAttr)
		cl.parentClass = "Aaa0"
		return cl

	def testAttribute(self):
	    self.isCompiling(self.basicClass("", ""))
	    self.isCompiling(self.basicClass("int", "param1"))
	    self.isCompiling(self.basicClass("int*", "param2"))
	    self.isCompiling(self.basicClass("int const", "param3"))
	    self.isCompiling(self.basicClass("int const*", "param4"))
	    self.isCompiling(self.basicClass("int ***", "param5"))
	    self.isCompiling(self.basicChildClass("", ""))

	def testInheritance(self):
		pass

if __name__ == '__main__':
	unittest.main()
