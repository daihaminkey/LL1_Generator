import CodeGenerator
from Grammar import Grammar


file = open("output/Grammar.txt", 'r')
data = file.read().replace(' ','').replace('\t','').replace('\n',';')
file.close()

grammar = Grammar(data)

file = open('output/Output.py', 'w')

file.write(CodeGenerator.gen_basic())
for rule in grammar.get_rules():
	file.write(CodeGenerator.gen_rule(rule))

file.write(CodeGenerator.gen_main())
file.close()
