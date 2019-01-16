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
		self.root()

	def _26(self):
		if self.ch in ['2', '6']:
			if self.ch == '2':
				self.read()
			if self.ch == '6':
				self.read()
		else:
			self.error()

	def _48(self):
		if self.ch in ['4', '8']:
			if self.ch == '4':
				self.read()
			if self.ch == '8':
				self.read()
		else:
			self.error()

	def _048(self):
		if self.ch in ['0', '4', '8']:
			if self.ch == '0':
				self.read()
			if self.ch in ['4', '8']:
				self._48()
		else:
			self.error()

	def _13579(self):
		if self.ch in ['1', '3', '5', '7', '9']:
			if self.ch == '1':
				self.read()
			if self.ch == '3':
				self.read()
			if self.ch == '5':
				self.read()
			if self.ch == '7':
				self.read()
			if self.ch == '9':
				self.read()
		else:
			self.error()

	def x_odd(self):
		if self.ch in ['1', '3', '5', '7', '9', '2', '6', '0', '4', '8']:
			if self.ch in ['1', '3', '5', '7', '9']:
				self._13579()
				self.x_odd()
			if self.ch in ['2', '6']:
				self._26()
				self.fin()
			if self.ch in ['0', '4', '8']:
				self._048()
				self.x_even()
		else:
			self.error()

	def x_even(self):
		if self.ch in ['1', '3', '5', '7', '9', '2', '6', '0', '4', '8']:
			if self.ch in ['1', '3', '5', '7', '9']:
				self._13579()
				self.x_odd()
			if self.ch in ['2', '6']:
				self._26()
				self.x_even()
			if self.ch in ['0', '4', '8']:
				self._048()
				self.fin()
		else:
			self.error()

	def fin(self):
		if self.ch in ['1', '3', '5', '7', '9', '2', '6', '0', '4', '8']:
			if self.ch in ['1', '3', '5', '7', '9']:
				self._13579()
				self.x_odd()
			if self.ch in ['2', '6']:
				self._26()
				self.x_even()
			if self.ch in ['0', '4', '8']:
				self._048()
				self.fin()

	def root(self):
		if self.ch in ['1', '3', '5', '7', '9', '2', '6', '4', '8']:
			if self.ch in ['1', '3', '5', '7', '9']:
				self._13579()
				self.x_odd()
			if self.ch in ['2', '6']:
				self._26()
				self.x_even()
			if self.ch in ['4', '8']:
				self._48()
				self.fin()
		else:
			self.error()


grammar = Grammar()
try:
	grammar.run('%INSERT YOUR STRING HERE%')
	print()
except:
	print('String is not a part of the given grammar')
else:
	print('String is a part of the given grammar')

