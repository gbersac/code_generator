import os
import sys

def main():
	className = raw_input('Enter class name: ')

	fileName = className + ".cpp"
	if os.path.exists("src"):
		open("src/" + fileName, "a").close()
		print "src/" + fileName + " created"
	else:
		open(fileName, "a").close()
		print fileName + " created"

	fileName = className + ".hpp"
	if os.path.exists("inc"):
		open("inc/" + fileName, "a").close()
		print "inc/" + fileName + " created"
	else:
		open(fileName + ".hpp", "a").close()
		print fileName + " created"

main()
