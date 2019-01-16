from unittest import TestCase
from Grammar import Sequence, Options, Grammar


class TestSequence(TestCase):
	
	def test_char_sequence_init(self):
		token = 'symbols'
		seq = Sequence(token)
		self.assertEqual(token, seq.__str__())
		self.assertEqual(len(seq), len(token))
	
	def test_token_sequence_init(self):
		token = '<token>'
		seq = Sequence(token)
		self.assertEqual(token, seq.__str__())
		self.assertEqual(len(seq), 1)
	
	def test_complex_sequence_init(self):
		token = 'tokens<are><easy>to<use>.'
		seq = Sequence(token)
		self.assertEqual(token, seq.__str__())
		self.assertEqual(len(seq), 12)
	
	def test_straight_first_symbols(self):
		token = 'token'
		seq = Sequence(token)
		self.assertEqual(seq.get_first_symbols(None), 't')


class TestOptions(TestCase):
	def test_degenerate_init(self):
		token = '<only>one<option>'
		opt = Options(token)
		self.assertEqual(token, opt.__str__())
		self.assertEqual(len(opt), 1)
	
	def test_complex_init(self):
		token = 'aagf<nt>a<djn><,kz>kkl|<test>drive'
		opt = Options(token)
		self.assertEqual(token, opt.__str__())
		self.assertEqual(len(opt), 2)
	
	def test_straight_first_symbols(self):
		token = 'hello|there'
		opt = Options(token)
		self.assertEqual(opt.get_first_symbols(None), ['h', 't'])


class TestGrammar(TestCase):
	def test_straight_first_symbol(self):
		grammar = Grammar('<root>::=a|b')
		self.assertEqual(grammar.first_symbols,['a','b'])

	def test_simple_first_symbol(self):
		grammar = Grammar('<root>::=a|<b>;<b>::=b|c')
		self.assertEqual(grammar.first_symbols,['a','b','c'])
	
	def test_simple_recursive_first_symbol(self):
		grammar = Grammar('<root>::=a|<b>;<b>::=b|c|d<root>')
		self.assertEqual(grammar.first_symbols, ['a', 'b', 'c', 'd'])
	
	def test_first_first_conflict(self):
		with self.assertRaises(Exception):
			Grammar('<root>::=a|<b>;<b>::=b|<b>')

	def test_first_follow_conflict(self):
		with self.assertRaises(Exception):
			Grammar('<root>::=<A>ab;<A>::=a|~')
			