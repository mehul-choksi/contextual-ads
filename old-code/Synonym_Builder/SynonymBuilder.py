import numpy
import re

from scipy import spatial

import collections
import time

from random import randint
from time import sleep

from scraper import Scraper

nodes_to_synon = []

print("Building word embeddings")
PATH = "/home/sukhad/Workspace/Machine_learning/Embeddings/GloVe/glove.6B.100d.txt"
embeddings_dict = dict()
with open(PATH,'r') as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = numpy.asarray(values[1:], "float32")
        embeddings_dict[word] = vector
print("done")

def find_relevant_keywords(first_list, second_list, num=20):
    _relevant_words = dict()
    for word2 in second_list:
        score_list = list()
        for word1 in first_list:
            try:
                score_list.append(1 - spatial.distance.cosine(embeddings_dict[word1.lower()], embeddings_dict[word2.lower()]))
            except:
                continue
        if not len(score_list)==0:
            _relevant_words[word2] = max(score_list)
    return dict(collections.Counter(_relevant_words).most_common(num))

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
            for i in range(1,n):
                node = self.create_node(tags[i],curr)
                curr.children.add(node)
                print(curr.name + '->' + node.name)
                curr = node

        print('Root: ' + str([child.name for child in root.children]))

        print("keyword file")
        with open('keyword_file','r') as f_key:
            text = f_key.read().split('\n')
            i = 0
            while i<len(text)-1:
                self.map[text[i]]._visited = True
                i += 2

        print("links")
        with open('sukhad_links.txt','r') as f_links:
            text = f_links.read().split('\n')
            i = 0
            while i<len(text)-1:
                self.map[text[i]]._links = text[i+1][1:len(text[i+1])-1].split(',')
                nodes_to_synon.append(text[i])
                i += 2

        print("done")
        #ca = self.map['Clothing & Accessories']
        #if ca in ca.children:
        #    ca.children.remove(ca)
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
                curr.children.remove(curr)    #Remove child from itself
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

    def build_synonyms(self):
        scraper = Scraper()
        for node in list(self.map.keys())[1:6]:
            if self.map.get(node)._visited:
                self.map.get(node).get_synonyms(scraper)

    def build_synonyms_from_file(self,file_name):

        print('Building from synonyms')
        for entry in  nodes_to_synon:
            print(entry)
            if len(entry) == 0:
                continue

            curr = self.map.get(entry)

            if curr._visited:
                print("already visited")
                continue

            if curr._links == []:
                print("no links")
                continue

            links = curr._links
            scraper = Scraper()

            resp = {}
            counter = 0
            links_keywords_cache = {}


            for link in links:
                if counter > 20:
                    break
                print('Trying: ', link)
                link = link.replace('\'', '')
                tdict = None
                try:
                    tdict=links_keywords_cache[link]
                except KeyError:
                    tdict = scraper.get_keywords(link)
                    links_keywords_cache[link] = tdict
                #except ValueError:
                    #continue;
                #print('response: ', str(tdict))
                if len(str(tdict)) > 0:
                    for key in tdict.keys():
                        try:
                            resp[key].append(tdict[key])
                        except KeyError:
                            resp[key] = [tdict[key]]
                counter += 1

            print("writing to file")
            writer = open('keyword_file','a')
            writer.write(entry + '\n')
            writer.write(str(resp)+'\n')

            #break
    def process(self):
        self.jsonStr = self.jsonStr[1:]
        self.jsonStr = self.jsonStr.replace("\"children\":[,", "\"children\":[")
        self.jsonStr = self.jsonStr.replace(",}", "}")
        self.jsonStr = self.jsonStr.replace("[,", "[")


    def build_synonyms(self, file):

        output = {}

        f = open(file, "r")
        text = f.read().split('\n')

        # change this function
        def aggreagation(arg):
            return (sum(arg) / float(len(arg)))

        def calculate_score(num1, num2):
            return num1 * num2

        i = 0
        while i < len(text)-1:
            try:

                print(text[i])
                #print(text[i])

                text[i+1] = text[i+1].replace('nan','0.0')

                node = self.map[text[i]]
                keywords = eval(text[i+1])

                keywords_aggregated = {k : aggreagation(v) for k,v in keywords.items()}

                name = node.name.lower()
                name = re.sub("[^a-z](&)","",name)

                word_emb_output = find_relevant_keywords(name.split(), list(keywords_aggregated.keys()))

                #print("Embeddings: ", word_emb_output)

                synonyms = {k: calculate_score(word_emb_output[k], keywords_aggregated[k]) for k in list(word_emb_output.keys())}

                print(synonyms)
                #print("Aggregated: ",keywords_aggregated)

                output[text[i]] = synonyms
            except KeyError:
                print(i," -  - doesn't exist")
            except:
                print(i," -  some error")
            finally:
                i += 2

        with open("synonyms.txt","w") as f:
            f.write(str(output))

if __name__ == '__main__':
    t = Tree()
    t.read_and_build()
    #t.bfs()


    #t.treeToJSON(t.root)
    #t.process()
    #t.build_synonyms()
    #fileWrite = open('treej.json', 'w')

    #fileWrite.write(t.jsonStr)

    t.build_synonyms('keyword_file_formatted')

    #t.build_synonyms_from_file('sukhad_links')
