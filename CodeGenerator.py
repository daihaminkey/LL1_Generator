from Grammar import Grammar, Rule


def gen_basic():
	return """\
class Grammar:
	def __init__(self):
		self.ch = None
		self.pos = 0
		self.data = None
	
	def error(self):
		raise Exception('pos '+str(self.pos))
		
	def read(self):
		if self.pos < len(self.data):
			self.ch = self.data[self.pos]
			print(self.ch, end='')
			self.pos += 1
		else:
			self.ch = ' '
	
	def run(self, text):
		self.data = text
		self.pos = 0
		self.read()
		self.root()\
"""


def gen_main():
	return """\n\n
grammar = Grammar()
try:
	grammar.run('%INSERT YOUR STRING HERE%')
	print()
except:
	print('String is not a part of the given grammar')
else:
	print('String is a part of the given grammar')

"""


def gen_rule(token: Rule):
	no_empty = True
	first_symbols = token.first_symbols
	if '~' in first_symbols:
		first_symbols.remove('~')
		no_empty = False

	code = f"""

	def {token.get_name()}(self):
		if self.ch in {token.first_symbols}:"""
	for seq in token.optionSet.sequences:
		first_symbols = list(seq.elements[0].get_first_symbols())
		if '~' in first_symbols:
			first_symbols.remove('~')
		if seq.elements[0].token == '~':
			continue
		if seq.elements[0].isStr:
			code += f"""
			if self.ch == '{seq.elements[0].token}':"""
		else:
			code += f"""
			if self.ch in {first_symbols}:"""
		
		for element in seq.elements:
			if element.isStr:
				code += f"""
				self.read()"""
			else:
				code += f"""
				self.{element.rule.get_name()}()"""
	if(no_empty):
		code += f"""
		else:
			self.error()"""
	return code

