from Cheetah.Template import Template

class FieldType:
	CLASSUNIQUE = 0
	CLASSLIST = 1
	STRING = 2
	DATE = 3
	YESNO = 4
	DOUBLE = 5

	@staticmethod
	def toString(t):
		if FieldType.CLASSUNIQUE == t:
			return 'CLASSUNIQUE'
		if FieldType.CLASSLIST == t:
			return 'CLASSLIST'
		if FieldType.STRING == t:
			return 'STRING'
		if FieldType.DATE == t:
			return 'DATE'
		if FieldType.YESNO == t:
			return 'YESNO'
		if FieldType.DOUBLE == t:
			return 'DOUBLE'

	@staticmethod
	def toScalaType(t):
		if FieldType.CLASSUNIQUE == t:
			return 'Class'
		if FieldType.CLASSLIST == t:
			return 'Class'
		if FieldType.STRING == t:
			return 'String'
		if FieldType.DATE == t:
			return 'DateTime'
		if FieldType.YESNO == t:
			return 'Boolean'
		if FieldType.DOUBLE == t:
			return 'BigDecimal'

class Field:

	"""
	fieldType: enum of FieldType
	childs: Only if the field is of tpe class
	"""
	def __init__(self, name, fieldType, description, isMandatory = True, level = 0, childs = []):
		self.name = name
		self.level = level
		self.type = fieldType
		self.description = description
		self.isMandatory = isMandatory
		self.level = level
		self.childs = childs

	def isClass(self):
		return self.type == FieldType.CLASSUNIQUE or self.type == FieldType.CLASSLIST

	def preIndent(self):
		return '  ' * self.level

	def __str__(self):
		if self.type == FieldType.CLASSUNIQUE or self.type == FieldType.CLASSLIST:
			childsStr = list(map(lambda x: x.__str__(), self.childs))
			return self.preIndent() + self.name + ' ->\n' + "\n".join(childsStr)
		else:
			return self.preIndent() + self.name + '[' + FieldType.toString(self.type) + ']'

	def typeName(self):
		if self.type == FieldType.CLASSUNIQUE:
			return self.className()
		if self.type == FieldType.CLASSLIST:
			return 'Seq[' + self.className() + ']'
		elif self.isMandatory:
			return FieldType.toScalaType(self.type)
		else:
			return 'Option[' + FieldType.toScalaType(self.type) + ']'

	def xmlValidator(self):
		s = ''
		if self.type == FieldType.CLASSLIST:
			s = '__.read(JtoValidationUtils.seqXmlRule[{0}]("{1}"))'.format(self.className(), self.name)
		elif self.name == 'dateNaissance' and self.isMandatory:
			s = '(__ \ "{0}").read(dateTimeNaissanceRule)'.format(self.name)
		elif self.type == FieldType.DATE and self.isMandatory:
			s = '(__ \ "{0}").read(dateTimeRule)'.format(self.name)
		elif self.name == 'dateNaissance':
			s = '(__ \ "{0}").read(dateTimeNaissanceOptionRule)'.format(self.name)
		elif self.type == FieldType.DATE:
			s = '(__ \ "{0}").read(dateTimeOptionRule)'.format(self.name)
		elif self.type == FieldType.YESNO and self.isMandatory:
			s = '(__ \ "{0}").read(ouiNonRule)'.format(self.name)
		elif self.type == FieldType.YESNO:
			s = '(__ \ "{0}").read(ouiNonOptionRule)'.format(self.name)
		else:
			s = '(__ \ "{0}").read[{1}]'.format(self.name, self.typeName())
		return '      ' + s

	############################################################################
	######################### specific to class types ##########################

	def hasDateChild(self):
		for child in self.childs:
			if child.type == FieldType.DATE:
				return True
		return False

	def hasYesNoChild(self):
		for child in self.childs:
			if child.type == FieldType.YESNO:
				return True
		return False

	def className(self):
		name = self.name[0].upper() + self.name[1:]
		return name

	def classChildren(self):
		childs = []
		for child in self.childs:
			if child.isClass():
				childs.append(child)
		return childs

	def innerClassStr(self):
		def toInnerClass(field):
			toString = field.toScalaCaseClass()
			lines = toString.split('\n')
			return '\n'.join(map(lambda x: self.preIndent() + x, lines))
		classChildren = list(map(toInnerClass, self.classChildren()))
		return "".join(classChildren)

	def toScalaCaseClass(self):
		t = Template(file = 'case_class.tmpl', searchList=[{'class': self}])
		return str(t)

	def attributeList(self):
		def inCompanionObject():
			if self.level == 0:
				return ''
			else:
				return self.className() + '.'
		def childType(child):
			if child.type == FieldType.CLASSUNIQUE:
				return child.name + ': ' + inCompanionObject() + child.typeName()
			if child.type == FieldType.CLASSLIST:
				return child.name + ': Seq[' + inCompanionObject() + child.typeName()[4:]
			else:
				return child.name + ': ' + child.typeName()
		childsTypes = list(map(childType, self.childs))
		if self.childs <= 3:
			return ', '.join(childsTypes)
		else:
			return '\n  ' + ',\n  '.join(childsTypes) + '\n'

	def childsXmlValidator(self):
		if len(self.childs) > 1:
			validators = list(map(lambda x: x.xmlValidator(), self.childs))
			return '    (\n' + " ~\n".join(validators) + '\n   )(' + self.className() + '.apply)'
		else:
			validator = self.childs[0].xmlValidator()
			return '  ' + validator + '.map(' + self.className() + '.apply)'
