import unittest
from src.attributeModel import Attribute, PointerType

class TestSequenceFunctions(unittest.TestCase):
	def testConst(self):
		att = Attribute("const aaa", "bbb")
		self.assertEqual(att.isConst, True)
		att = Attribute(" const aaa", "bbb")
		self.assertEqual(att.isConst, True)
		att = Attribute("constaaa", "bbb")
		self.assertEqual(att.isConst, False)
		att = Attribute("aaaconst", "bbb")
		self.assertEqual(att.isConst, False)
		att = Attribute("aaaconstaaa", "bbb")
		self.assertEqual(att.isConst, False)
		att = Attribute("aaa const", "bbb")
		self.assertEqual(att.isConst, True)
		att = Attribute("aaa const*", "bbb")
		self.assertEqual(att.isConst, True)
		att = Attribute("aaa&const*", "bbb")
		self.assertEqual(att.isConst, True)
		att = Attribute("aaa&con*", "bbb")
		self.assertEqual(att.isConst, False)

	def testPointer(self):
		att = Attribute("*aaa", "bbb")
		self.assertEqual(att.ptrType, PointerType.POINTER)
		att = Attribute("aaa*", "bbb")
		self.assertEqual(att.ptrType, PointerType.POINTER)
		att = Attribute("aaa const*", "bbb")
		self.assertEqual(att.ptrType, PointerType.POINTER)
		att = Attribute("aaa", "bbb")
		self.assertEqual(att.ptrType, PointerType.NONE)
		att = Attribute("aaa***", "bbb")
		self.assertEqual(att.nbPtr, 3)

	def testReference(self):
		att = Attribute("&aaa", "bbb")
		self.assertEqual(att.ptrType, PointerType.REFERENCE)
		att = Attribute("aaa&", "bbb")
		self.assertEqual(att.ptrType, PointerType.REFERENCE)
		att = Attribute("aaa", "bbb")
		self.assertEqual(att.ptrType, PointerType.NONE)

if __name__ == '__main__':
	unittest.main()
