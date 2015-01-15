import unittest
import os
import shutil
import init
import subprocess

from attributeModel import Attribute, PointerType
from classModel import Class
from outputTemplate import OutputTemplate

TEST_DIR = "test_dir"
CMD_LINE = "g++ -Wall -Wextra -Werror -c "

class TestCompileFunctions(unittest.TestCase):
	def setUp(self):
		if not os.path.exists(TEST_DIR):
			os.makedirs(TEST_DIR)

	def tearDown():
		os.chdir(TEST_DIR)
		os.chdir("..")
		shutil.rmtree(TEST_DIR)

	def isCompiling(self, cl):
		OutputTemplate(cl)
		retcall = subprocess.call(CMD_LINE + cl.name + init.CPP_EXT)
		return (retcall == 0)

	def basicClass(self, typeAttr, nameAttr):
		cl = Class("Aaa")
		cl.addAttr(typeAttr, nameAttr)
		return cl

	def testAttribute(self):
		self.isCompiling(self.basicClass("int", "param1"))

if __name__ == '__main__':
	unittest.main()
