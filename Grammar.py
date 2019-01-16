from abc import ABC, abstractmethod
#TODO naming check
#TODO regexp check
#TODO space support


class Element(ABC):
	def __str__(self):
		return self.token

	@abstractmethod
	def get_first_symbols(self):
		pass

class ElementStr(Element):
	def __init__(self, data):
		self.token = data
		self.isStr = True
		
	def get_first_symbols(self):
		return self.token


class ElementRule(Element):
	def __init__(self, data):
		self.token = data
		self.isStr = False
		self.rule = None
	
	def get_first_symbols(self):
		return self.rule.get_first_symbols()
	
	def set_token_ref(self, token_db):
		for rule in token_db.rules:
			if rule == self.token:
				self.rule = token_db.rules[rule]
				#print('for token',self.token,'found rule',rule.optionSet)
				return
		raise Exception(self.token+': no rule found')
	

class Sequence:
	def __init__(self, token_string: str):
		self.elements = list()
		while len(token_string) > 0:
			l_bracket = token_string.find('<')
			if l_bracket == -1:
				for char in list(token_string):
					self.elements.append(ElementStr(char))
				token_string = ''
			else:
				if l_bracket != 0:
					for char in list(token_string[0:l_bracket]):
						self.elements.append(ElementStr(char))
				
				r_bracket = token_string.find('>')
				self.elements.append(ElementRule(token_string[l_bracket:r_bracket + 1]))
				token_string = token_string[r_bracket + 1:]

	def __len__(self):
		return len(self.elements)
	
	def __str__(self):
		tokens = list()
		for token in self.elements:
			tokens.append(token.__str__())
		return ''.join(tokens)
	
	def set_token_refs(self, token_db):
		for element in self.elements:
			if not element.isStr:
				element.set_token_ref(token_db)
				
		# first-follow conflict detection
		
		for i in range(0,len(self.elements)):
			if i != len(self.elements)-1:
				if not self.elements[i].isStr:
					first_symbols = self.elements[i].get_first_symbols()
					if '~' in first_symbols:
						first_symbols.remove('~')
						follow_symbols = list(self.elements[i+1].get_first_symbols())
						conflict = [value for value in first_symbols if value in follow_symbols]
						if len(conflict) > 0:
							raise Exception(f'First-follow conflict found in sequence {self}. Duplicated symbols in inner can-be-empty token: {conflict}')
				
	def get_first_symbols(self,rule_name):
		if rule_name == self.elements[0].token:
			raise Exception(f'Left recursion found in {rule_name} ::= {self}|...')
		return self.elements[0].get_first_symbols()


class Options:
	def __init__(self, token_string):
		tokens = token_string.split('|')
		self.sequences = list()
		for token in tokens:
			self.sequences.append(Sequence(token))
		
	def __str__(self):
		sequences_str = list()
		for sequence in self.sequences:
			sequences_str.append(sequence.__str__())
		return '|'.join(sequences_str)
	
	def set_token_refs(self, token_db):
		for sequence in self.sequences:
			sequence.set_token_refs(token_db)

	def __len__(self):
		return len(self.sequences)
	
	def get_first_symbols(self, rule_name):
		symbols = list()
		for seq in self.sequences:
			symbols.extend(seq.get_first_symbols(rule_name))
		return symbols
		

class Rule:
	def __init__(self, str):
		self.row_data = str
		lr = str.split('::=')
		self.name, self.optionSet = lr[0], Options(lr[1])
		self.first_symbols = None
	
	def __str__(self):
		return self.name + '::=' + self.optionSet.__str__()
	
	def set_token_refs(self, token_db):
			self.optionSet.set_token_refs(token_db)
		
	def get_first_symbols(self):
		if self.first_symbols is None:
			self.first_symbols = self.optionSet.get_first_symbols(self.name)
			if len(self.first_symbols) > len(set(self.first_symbols)):
				raise Exception(f'Rule {self.row_data} is not LL1 rule. First symbols duplication: {self.first_symbols}')
		return self.first_symbols
		
	def get_name(self):
		return self.name[1:-1]


class TokenDB:
	def __init__(self):
		self.rules = {}
		
	def __len__(self):
		return len(self.rules)
	
	def append(self,rule):
		self.rules[rule.name]=rule
	
	def get_root(self):
		return self.rules['<root>']
	
	def get_rules(self):
		return self.rules.values()
		
		
class Grammar:
	def __init__(self, grammar):
		print('Parsing grammar...')
		self.tokenDB = TokenDB()
		tokens = grammar.split(';')
		for token in tokens:
			rule = Rule(token)
			self.tokenDB.append(rule)
		print(f'\t{len(tokens)} tokens parsed')
		
		for rule in self.tokenDB.get_rules():
			rule.set_token_refs(self.tokenDB)
		print('\tToken references configured')
		
		for rule in self.tokenDB.get_rules():
			rule.get_first_symbols()
		
		self.first_symbols = self.get_root().first_symbols
		print('\tFirst symbols generated without conflict\nDone!\n')
			
	def __str__(self):
		ret = ''
		for token in self.tokenDB.rules:
			ret += f'{token.__str__()};'
		return ret
			
	def print(self):
		print(len(self.tokenDB), 'tokens stored:\n', str.replace(self.__str__(),';','\n '))
		
	def get_root(self):
		return self.tokenDB.get_root()

	def get_rules(self):
		return self.tokenDB.get_rules()

