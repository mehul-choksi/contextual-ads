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
			#for i in range(1,min(3,n)):	#visualizer mode
			for i in range(1,n):		#mapper mode				
				node = self.create_node(tags[i],curr)
				curr.children.add(node)
				print(curr.name + '->' + node.name)
				curr = node

		print('Root: ' + str([child.name for child in root.children]))

		
	def bfs(self):

		root = self.root
		dq = collections.deque()

		dq.appendleft(root)
		visited = set()
		
		while dq:

			curr = dq.popleft()
			if curr in curr.children:
				curr.children.remove(curr)	#Remove child from itself

			print(curr.name)
			
			currCh = curr.children
			filteredCh = set()

			for child in currCh:
				if child.parent != curr.name:
					continue
				else:
					dq.appendleft(child)
					filteredCh.add(child)
			curr.children = filteredCh

	def treeToJSON(self,curr):
		self.jsonStr += ",{\"name\":" + "\"" + curr.name + "\","

		self.jsonStr += "\"narent\":" + "\"" + curr.parent + "\","
		if len(curr.children) > 0:
			self.jsonStr += "\"children\":[" 
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
