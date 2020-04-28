import numpy
import re


from scipy import spatial

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
        self._links = list()

    def get_synonyms(self ,scraper=Scraper()):
        i = 0
        print(self.name)
        #print(self._links)
        keyword_list = []
        for link in self._links:
            print(link)
            link = link.replace("'","").strip()
            try:
                keywords = scraper.get_keywords(site=link)
                #print(set(keywords.keys()))
                keyword_list += list(keywords.keys())
                i += 1
                if i%10==0:
                    break;
            except:
                continue

        keyword_list = set(keyword_list)
        name_list = self.name.split(" & ")

        self.synonyms = find_relevant_keywords(name_list, keyword_list, 20)
        print(self.synonyms)

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
#            print(root.name + '->' + curr.name)
            #for i in range(1,min(3,n)):    #visualizer mode
            for i in range(1,n):        #mapper mode
                node = self.create_node(tags[i],curr)
                curr.children.add(node)
#                print(curr.name + '->' + node.name)
                curr = node

#        print('Root: ' + str([child.name for child in root.children]))

        with open("search_links.txt","r") as f:
            text = f.read().split('\n')
            i = 0
            while i<len(text)-1:
                self.map[text[i]]._visited = True
                self.map[text[i]]._links = text[i+1][1:len(text[i+1])-1].split(",")
                #print(self.map[text[i]]._links)
                i += 2


    def build_synonyms(self):
        scraper = Scraper()
        for node in list(self.map.keys())[1:16]:
            if self.map.get(node)._visited:
                self.map.get(node).get_synonyms(scraper)



    def bfs(self):

        # this to be commented later
        #
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
                curr.children.remove(curr)    #Remove child from itself

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


    def get_links_from_list(self):
        """DELETE THIS SHIT"""
        node_list = ['Health Supplies', 'Houses & Habitats', 'Fish & Aquatics', 'Breeding Tanks', 'Food', 'Aquarium Décor', 'Aquarium Starter Kits', 'Automatic Feeders', 'Aquarium Lights', 'Hydrometers', 'Water Treatments', 'Cleaners', 'Test Kits', 'Fish Bowls', 'Aquarium Heaters & Chillers', 'Medication & Health Supplies', 'Grocery & Gourmet Foods', 'Rice', 'Flour & Pulses', 'Red Rice', 'Sona Masuri', 'Brown Rice', 'Basmati', 'Poha (Flattened Rice)', 'Pasta & Noodles', 'Pasta', 'Noodles', 'Dried Fruits', 'Mixed Dried Fruits', 'Raisins', 'Berries', 'Nuts & Seeds', 'Anjeer (Figs)', 'Apricots', 'Prunes', 'Mangos', 'Dates', 'Canned & Jarred Food', 'Meat', 'Fruits', 'Soups', 'Vegetables', 'Olives', 'Pulses & Beans', 'Cooking & Baking Supplies', 'Cooking Pastes & Sauces', 'Baking Supplies', 'Vinegars', 'Syrups', 'Oils & Ghee', 'Salad Dressings', 'Jams', 'Honey & Spreads', 'Coffee', 'Tea & Beverages', 'Cereal & Muesli', 'Childrens Cereals', 'Cereal & Snack Bars', 'Granola Cereals', 'Oats & Porridge', 'Muesli', 'Flakes', 'Pickles', 'Mixed Pickles', 'Garlic', 'Mango', 'Ginger', 'Lime', 'Chillies', 'Chutneys', 'Gooseberry', 'Snack Foods', 'Trail Mix', 'Granola & Snack Bars', 'Salsas', 'Rice Cakes', 'Biscuits & Cookies', 'Puffed Snacks', 'Fruit Snacks', 'Popcorn', 'Hampers & Gourmet Gifts', 'Sweets Gifts', 'Chocolate Gifts', 'Tea Gifts', 'Sweets', 'Chocolate & Gum', 'Trackpants & Joggers', 'Rainwear', 'Dungarees', 'Telephones & Accessories', 'Landline Phones', 'Answering Machines', 'VOIP Phones', 'GPS & Accessories', 'Motorcycle GPS', 'GPS Trackers', 'Truck GPS', 'Car GPS', 'Marine GPS', 'Mobiles & Tablets', 'Smartphones & Basic Mobiles', 'Portable Media Players', 'DVD & Blu-ray Players', 'Radios', 'Boomboxes', 'MP3/MP4 Players', 'Cameras & Photography', 'Video Cameras', 'Film Cameras', 'Cases & Bags', 'DSLR Cameras', 'Car & Vehicle Electronics Accessories', 'Home Theatre', 'TV & Video', 'Hi-Fi & Home Audio', 'Receivers & Separates', 'Radios & Boomboxes', 'Speakers', 'Compact Stereos', 'Wearable Technology', 'Smartwatches & Accessories', 'Headphones', 'Over-Ear', 'On-Ear', 'In-Ear', 'Arts', 'Film & Photography', 'Historical Fiction', 'Games', 'Comics & Mangas', 'Family', 'Language Learning', 'Humour', 'Interactive & Activity Books', 'Mysteries & Curiosities', 'Literature & Fiction', 'Language', 'Linguistics & Writing', 'Business & Economics', 'Business', 'Business Self-Help', 'Economics', 'Industries & Business Sectors', 'Computing', 'Internet & Digital Media', 'Table Tennis', 'Hurling', 'Biographies', 'Diaries & True Accounts']

        with open("search_links.txt","r") as f:
            text = f.read().split('\n')
            i = 0
            while i<len(text)-1:
                self.map[text[i]]._visited = True
                self.map[text[i]]._links = text[i+1][1:len(text[i+1])-1].split(",")
                    #print(self.map[text[i]]._links)
                i += 2

        scraper = Scraper()

        i = 0
        for node in node_list:
            print(node)
            curr = self.map.get(node)
            if (curr is not self.root) and (not curr._visited):
                i += 1
                links = curr.get_links(scraper)
                with open("search_links.txt","a+") as f:
                    f.write(curr.name+"\n")
                    f.write(str(links)+"\n")
                    sleep(randint(2,10))

                if i%30==0:
                    return
                if i%15==0:
                    del scraper
                    scraper = Scraper()
            else:
                print("already visited")


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
    #t.bfs()
    t.build_synonyms()
    #t.get_links_from_list()
    #t.treeToJSON(t.root)
    #t.process()

    #fileWrite = open('treej.json', 'w')
    #fileWrite.write(t.jsonStr)
