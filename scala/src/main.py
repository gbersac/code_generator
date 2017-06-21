#! /usr/local/bin/python
import csv
import sys

from parser import parse
from toFile import toFile, toRootFile
from field import Field, FieldType

def main():
	if len(sys.argv) != 2:
		print("Error input file as argument required.")
	inputFile = sys.argv[1]
	with open(inputFile, 'rb') as f:
		reader = csv.reader(f, delimiter=';', quotechar='\'')
		lines = list(reader)
		fields = parse(lines[1:]) # first line is headers
		# for field in fields:
		# 	print field
		globalField = Field("OMDEMessage", FieldType.CLASSUNIQUE, '', True, 0, fields)
		toRootFile(globalField)
		for field in fields:
			if field.isClass():
				toFile(field)

main()
