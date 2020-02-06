import collections 
import time
class Node():

	def __init__(self,name='',parent='',children=set()):
		self.name = name
		self.parent = parent
		self.children = children
	def print_node(self):
		return 'Name: '+self.name+' Children: ' + ' Parent: ' + self.parent + str([node.name for node in self.children])


class Tree():

	def __init__(self):
		self.root = Node(name='root',children=set())
		self.source_file = 'tags.txt'
		self.map = {}
		self.map['root'] = self.root
		self.jsonStr = ""
		#self.logger = open('logs.txt', 'a')

	def create_node(self,name,parent):
		try:
			node = self.map[name]
			return node
		except:
			node = Node(name,parent=parent.name)
			parent.children.add(node)
			node.parent = parent.name		
			self.map[name] = node	
			return node

	def read_and_build(self):
		reader = open(self.source_file)
		root = self.root
		for line in reader:
			line = line.strip()
			line = line.replace('\'','')
			line = line.replace("\"", '')
			tags = line.split(', ')
			
			n = len(tags)
			
			
			curr = self.create_node(tags[0],root)
			print(root.name + '->' + curr.name)
			for i in range(1,min(3,n)):
				node = self.create_node(tags[i],curr)
				curr.children.add(node)
				print(curr.name + '->' + node.name)
				curr = node

		print('Root: ' + str([child.name for child in root.children]))

		#ca = self.map['Clothing & Accessories']
		#if ca in ca.children:
		#	ca.children.remove(ca)
		#print('Clothes: ' + str([child.name for child in ca.children]))
		#boys = self.map['Boys']
		#boys.children.remove(boys)
		#print('Boys: ' + str([child.name for child in boys.children]))
	def bfs(self):
		#print('bfs')
		root = self.root
		dq = collections.deque()

		dq.appendleft(root)
		visited = set()
		
		while dq:
			#time.sleep(0.01)
			curr = dq.popleft()
			if curr in curr.children:
				curr.children.remove(curr)	#Remove child from itself
				#print('Removed redundancy')
			print(curr.name)
			
			currCh = curr.children
			#print(str([child.name for child in currCh]))
			filteredCh = set()

			for child in currCh:
				if child.parent != curr.name:
					#print('Parent of ', child.name , ' is ', child.parent)
					continue
				else:
					#print(child.name, ' is child of ', curr.name)
					dq.appendleft(child)
					filteredCh.add(child)
			curr.children = filteredCh

		#print('bfs end')

	def treeToJSON(self,curr):
		self.jsonStr += ",{\"name\":" + "\"" + curr.name + "\","
		#print("{\"Name\":" + "\"" + curr.name + "\",")
		self.jsonStr += "\"narent\":" + "\"" + curr.parent + "\","
		#print("\"Parent\":" + "\"" + curr.parent + "\",")
		if len(curr.children) > 0:
			self.jsonStr += "\"children\":[" 
			# Children 
			currChildren = curr.children

			for c in currChildren:
				self.treeToJSON(c)
			self.jsonStr += "]}"

		else:
			self.jsonStr += "}"

	
	def process(self):
		self.jsonStr = self.jsonStr[1:]
		self.jsonStr = self.jsonStr.replace("\"children\":[,", "\"children\":[")
		self.jsonStr = self.jsonStr.replace(",}", "}")
		self.jsonStr = self.jsonStr.replace("[,", "[")
if __name__ == '__main__':
	t = Tree()
	t.read_and_build()
	t.bfs()

	t.treeToJSON(t.root)
	t.process()

	fileWrite = open('treej.json', 'w')
	fileWrite.write(t.jsonStr)
