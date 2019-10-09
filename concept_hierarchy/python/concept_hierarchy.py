from collections import deque
from time import sleep
class Node():
	def __init__(self, name):
		self.name = name
		self.parent = 0
		self.children = set()
		self.confidence = 0;

	def printNode(self):
		print(self.name + ' ' + str(self.confidence))

class ConceptHierarchy():
	
	def __init__(self,path,file_name):
		self.path = path
		self.file_name = file_name
		self.lookup = {}
		root = Node("Root")
		self.lookup["Root"] = root

	def create_read(self):
		reader = open(path + file_name, 'r')
		#lookup = self.lookup
		#first create all objects

		for line in reader:
			line = line.rstrip()
			#print(line)
			if line.startswith("[NewConcept]"):
				#print(line)
				tokens = line.split(' ')
				node = Node(tokens[1])
				self.lookup[tokens[1]] = node
				print('Created node with name: ' + self.lookup[tokens[1]].name)
			
			
		reader.close()
	
	
	def read(self):

		self.create_read()

		reader = open(path + file_name, 'r')

		
		print("**** Links ****")
		for line in reader:
			line = line.rstrip()

			if line.startswith("[Parent]"):
				tokens = line.split(' ')
				tokens = [token for token in tokens if token != '']		
				curr = tokens[1]
				curr_node = self.lookup[curr]
				parent = tokens[2]	
				parent_node = self.lookup[parent]
				curr_node.parent = parent_node
				#print("[" + parent_node.name + "] " + "-> " + curr_node.name)
				parent_node.children.add(curr_node)		
			elif line.startswith("[Children]"):
				tokens = line.split(' ')
				curr = tokens[1]
				curr_node = self.lookup[curr]				
				n = len(tokens)
				print("Children for "+ curr +":  ", end = "")
				if n < 2:
					continue
				for i in range(2,n):
					curr_node.children.add(self.lookup[tokens[i]])
					#self.lookup[tokens[i]].parent = curr_node
					print (tokens[i], end = " ")
				print()
					
	def check(self): #Validate if the links are established
		print("Checking...")
		val = self.lookup["Laptop"]
		myList = val.children
		for entry in myList:
			print(entry.name)

	def allocate_confidence(self):
		q = deque()
		root = self.lookup["Root"]
		root.confidence = 0.1	#Fixed val
		root_children = root.children
		for root_child in root_children:
			root_child.confidence = 0.5
			q.append(root_child)
		while q:
			node = q.popleft()
			print("Traversing: " + node.name)
			children = node.children
			print("Children: ", end = "")
			for child in children:
				print(child.name, end=" ")
				q.append(child)
			print()
			parent_conf = node.parent.confidence
			if node not in root_children:
				node.confidence = parent_conf + (1 - parent_conf)/2

	def traverse(self):
		q = deque()
		root = self.lookup["Root"]
		q.append(root)
		while q:
			node = q.popleft()
			node.printNode()
			children = node.children
			for child in children:
				q.append(child)

	def similar(self, topic1, topic2):
		set1 = set()
		set2 = set()
		root = self.lookup['Root']
		set1.add(root)
		set2.add(root)
		try:
			node1 = self.lookup[topic1]
			node2 = self.lookup[topic2]
			while node1 != root:
				set1.add(node1)
				node1 = node1.parent
			while node2 != root:
				set2.add(node2)
				node2 = node2.parent

			curr_match = root
			for entry in set1:
				if entry in set2:
					if entry.confidence > curr_match.confidence:
						curr_match = entry

			print("Matched node: ")
			curr_match.printNode()
				
		except KeyError:
			print('No such topic exists')

	def generate_scrapper_queries(self):
		q = deque()
		root = self.lookup["Root"]
		q.append(root)
		while q:
			node = q.popleft()
			children = node.children
			if len(children) == 0:
				self.write_path(node)
			for child in children:
				q.append(child)

	def write_path(self, node):
		nodepath = ""
		root = self.lookup["Root"]
		while node != root:
			nodepath = node.name + " " + nodepath
			node = node.parent

		writer = open("scrapper_queries", "a")
		writer.write(nodepath + "\n")

	def concept_match(self, keywords_matched):
		final_matches = {}
		root = self.lookup["Root"]
		keyword_node = root
		for key in keywords_matched:
			keyword_conf = keywords_matched[key]
			print("keyword conf: " + str(keyword_conf))
			try:
				keyword_node = self.lookup[key.lower()]
			except KeyError:
				keyword_node = root
			finally:
				keyword_node.printNode()
				net_conf =  keyword_node.confidence * keyword_conf
				final_matches[key.lower()] = net_conf
		return final_matches
			

path = '/home/ash/Desktop/POC-1/concept_hierarchy/python/'
file_name = 'input_hierarchy'
"""
concept = ConceptHierarchy(path, file_name)
concept.read()
concept.check()
concept.allocate_confidence()
concept.traverse()
concept.similar("Laptop", "TV")
concept.generate_scrapper_queries()
"""
