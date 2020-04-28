import collections 
import time
import sys
sys.setrecursionlimit(99999)
class Node():

	def __init__(self,name='',parent='',children=set()):
		self.name = name
		self.parent = parent
		self.children = children
	def print_node(self):
		return 'Name: '+self.name+', Parent: '+self.parent+' Children: '+ str([node.name for node in self.children])


class Tree():

	def __init__(self):
		self.root = Node(name='root',parent='',children=set())
		self.source_file = 'testtags.txt'
		self.map = {}
		self.map['root'] = self.root
		self.jsonStr = ""
		self.checker = set()
		self.logger = open('logs.txt', 'a')
	def insert(self,name,parent):
		
		try:
			node = self.map[name]
			return
		except:
			node = None
			
			node = Node(name=name,parent=parent)
			parentNode = self.map[parent]
			parentNode.children.add(node)
							
			self.map[name] = node
			
		print('Added: ', parent , '->', name)

	def read_and_build(self):
		reader = open(self.source_file)
		for line in reader:
			line = line.strip()
			line = line.replace('\'','')
			line = line.replace("\"", '')
			tags = line.split(', ')
			
			self.insert(tags[0],'root')
			n = len(tags)
			for i in range(1,n):
				self.insert(tags[i],tags[i-1])	

	def validate(self):

		dq = collections.deque()

		dq.appendleft(self.root)

		checker = set()
		while dq:
			#time.sleep(0.01)
			curr = dq.popleft()
			while dq and curr.name in checker:
				curr = dq.popleft()
				#print('[Redundant]: ', curr.name)
					
			print(curr.name)
			#print([node.name for node in curr.children])
			checker.add(curr.name)
			currChildren = curr.children
			for c in currChildren:
				if c.name in checker:
					continue
				dq.appendleft(c)
			if not dq:
				return

	def dfs(self,curr):
		self.logger.write(curr.print_node())
		if curr in curr.children:
			curr.children.remove(curr)
		for c in curr.children:
			self.dfs(c)
		

	def bfs(self):
		root = self.root
		dq = collections.deque()

		dq.appendleft(root)
		
		while dq:
			#time.sleep(0.01)
			curr = dq.popleft()
			if curr in curr.children:
				curr.children.remove(curr)	#Remove child from itself
			
			print(curr.name)
			
			currCh = curr.children
			for child in currCh:
				dq.appendleft(child)

	def treeToJSON(self,curr):
		self.jsonStr += ",{\"Name\":" + "\"" + curr.name + "\","
		self.checker.add(curr.name)
		#print("{\"Name\":" + "\"" + curr.name + "\",")
		self.jsonStr += "\"Parent\":" + "\"" + curr.parent + "\","
		#print("\"Parent\":" + "\"" + curr.parent + "\",")
		if len(curr.children) > 0:
			self.jsonStr += "\"Children\":[" 
			# Children 
			currChildren = curr.children

			for c in currChildren:
				if c.name not in self.checker:
					self.treeToJSON(c)
					#self.jsonStr += ",{\"Name\":" + "\"" + c.name + "\","
					#self.jsonStr += "\"Parent\":" + "\"" + c.parent + "\","
					#self.checker.add(c.name)
			self.jsonStr += "]}"
			#print("]}")
		else:
			self.jsonStr += "}"
			#print("}")
	
	def process(self):
		self.jsonStr = self.jsonStr.replace("\"Children\":[,", "\"Children\":[")
			
if __name__ == '__main__':
	t = Tree()
	t.read_and_build()
	t.bfs()
	#t.treeToJSON(t.root)
	#writer = open('treeJSON.json', 'w')
	#t.process()

	#writer.write(t.jsonStr)
	#t.logger.close()

