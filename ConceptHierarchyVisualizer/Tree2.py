
import collections
import time

from random import randint
from time import sleep

from scraper import Scraper
from scrape_synonyms import SearchScraper

class Node():

	def __init__(self,name='',parent='',children=set(), confidence=None):
		self.name = name
		self.parent = parent
		self.children = children
		self.confidence = confidence
		self.synonyms = dict()
		self._visited = False

	def get_synonyms(self,  searchScraper):
		scraper = Scraper()
		print("==",self.name,"==")
		if self.parent == "root":
			query = self.name + " blog"
		else:
			query = self.name + " " + self.parent + " blog"
		links = searchScraper.get_search_results_links(query)
		keyword_list = []
		for link in links:
			print(link)
			try:
				keywords = scraper.get_keywords(site=link)
				print(keywords.keys())
				keyword_list.append(keywords.keys())
			except:
				continue
		print(keyword_list)

	def get_links(self, scraper):
		name = self.name.replace("&","and")
		parent = self.parent.replace("&","and")
		query = ""
		if parent == "root":
			query = name + " blog"
		else:
			query = name + " " + parent + " blog"

		links = scraper.get_search_results_links(query)
		#print(links)
		return links

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

		# this to be commented later
		with open("search_links.txt","r") as f:
			text = f.read().split('\n')
			i = 0
			while i<len(text)-1:
				self.map[text[i]]._visited = True
				i += 2

		searchScraper = SearchScraper()
		scraper = Scraper()

		root = self.root
		dq = collections.deque()

		dq.appendleft(root)
		visited = set()

		i = 1
		while dq:

			# this will be removed in future
			if i==30:
				return

			if i%15==0:
				print("Hey!! We are gonna pull a little sneaky on Google. I am starting a new session")
				del scraper
				scraper = Scraper()

			curr = dq.popleft()
			if curr in curr.children:
				curr.children.remove(curr)	#Remove child from itself

			print(curr.name)
			if (curr is not self.root) and (not curr._visited):
				i += 1
				links = curr.get_links(scraper)
				with open("search_links.txt","a+") as f:
					f.write(curr.name+"\n")
					f.write(str(links)+"\n")

					sleep(randint(2,10))

			else:
				print("already-visited")

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
