class ConceptGenerator():

	def __init__(self, file_name):
		self.file_name = file_name
	def create_concept(self):

		name = input("Enter the name of concept: ").lower()
		parent = input("Enter the name of parent: ").lower()
		children_input = input("Enter children seperated by comma: ").lower()
		children = children_input.split(',')
		synonym_input = input("Enter the synonyms seperated by comma: ").lower()
		synonym = synonym_input.split(',')
		writer = open(file_name, 'a')
		writer.write('[NewConcept],' + name + '\n')
		writer.write('[Parent],' + name + ',' + parent + '\n')
		writer.write('[Children],' + name + ',' + ','.join(child.strip() for child in children) + '\n')
		writer.write('[Synonym],' + name + ',' + ','.join(syno.strip() for syno in synonym) + '\n')

file_name = "sample-concepts-2"
concept = ConceptGenerator(file_name)

num = int(input("Enter the number of concepts to be created: "))

for i in range(0,num):
	concept.create_concept()
