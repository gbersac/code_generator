import unittest
import os
import shutil
import init
import subprocess
import shlex

from attributeModel import Attribute, PointerType
from classModel import Class
from outputTemplate import OutputTemplate

TEST_DIR = "test_dir"
CMD_LINE = "gcc -Wall -Wextra -Werror -c "

class TestCompileFunctions(unittest.TestCase):

	def setUp(self):
		self.headerPath = "../" + OutputTemplate.outputImplementation
		self.implPath = "../" + OutputTemplate.outputHeader
		if not os.path.exists(TEST_DIR):
			os.makedirs(TEST_DIR)
		os.chdir(TEST_DIR)

	def isCompiling(self, cl):
		ot = OutputTemplate(cl)
		ot.outputImplementation = self.headerPath
		ot.outputHeader = self.implPath
		ot.process()
		cmd = shlex.split(CMD_LINE + cl.name + init.CPP_EXT)
		self.assertEqual(subprocess.call(cmd), 0)

	def basicClass(self, typeAttr, nameAttr):
		cl = Class("Aaa")
		cl.addAttr(typeAttr, nameAttr)
		return cl

	def testAttribute(self):
		self.isCompiling(self.basicClass("int", "param1"))

if __name__ == '__main__':
	unittest.main()
