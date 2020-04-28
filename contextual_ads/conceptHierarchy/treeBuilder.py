"""
TreeBuilder class:
    - tags to tree
    - add links to tree
    - add synonyms to tree

    functions we may never use :P
    - links to keywords

"""
import sys
sys.path.insert(0, "/home/sukhad/Workspace/GithHub/contextual-ads/contextual_ads")

import re

from tree import Tree
from scraper.scraper import Scraper
from wordEmbeddings.wordEmbeddings import Embeddings

class TreeBuilder:

    @staticmethod
    def build_tree_from_tags(tree, filepath):
        """
        Build tree from given tags file
        Args:
            tree: Tree, Tree object
            filepath: str, path of tags file

        Returns:
            None
        """

        reader = open(filepath)
        root = tree.root
        for line in reader:
            line = line.strip()
            line = line.replace('\'','')
            line = line.replace("\"", '')
            tags = line.split(', ')

            n = len(tags)

            curr = tree.create_node(tags[0],root)
            #print(root.name + '->' + curr.name)
            for i in range(1,n):
                node = tree.create_node(tags[i],curr)
                curr.children.add(node)
                #print(curr.name + '->' + node.name)
                curr = node

        #print('Root: ' + str([child.name for child in root.children]))


    @staticmethod
    def build_links_from_file(tree, search_links_file):
        """
        Build links from given search links file

        Args:
            tree: Tree, Tree object
            search_links_file: str, path of search links file

        Returns:
            None
        """
        with open(search_links_file ,'r') as f_links:
            text = f_links.read().split('\n')
            i = 0
            while i<len(text)-1:
                try:
                    tree.map[text[i]].links = text[i+1][1:len(text[i+1])-1].split(',')
                    i += 2
                except:
                    continue


    @staticmethod
    def build_synonyms_from_file(tree, keyword_file):
        """
            Build synonyms for tree
            Args:
                tree: Tree, Tree object
                filepath: str, path of keyword_file file

            Returns:
                None
        """

        embeddings = Embeddings()

        f = open(keyword_file, "r")
        text = f.read().split('\n')

        # change this function
        def aggreagation(arg):
            return (sum(arg) / float(len(arg)))

        def calculate_score(num1, num2):
            return num1 * num2

        i = 0
        while i < len(text)-1:
            try:
                #print(text[i])
                text[i+1] = text[i+1].replace('nan','0.0')

                node = tree.map[text[i]]
                keywords = eval(text[i+1])

                keywords_aggregated = {k : aggreagation(v) for k,v in keywords.items()}
                name = node.name.lower()
                name = re.sub("[^a-z](&)","",name)

                word_emb_output = embeddings.find_relevant_keywords(name.split(), list(keywords_aggregated.keys()))

                synonyms = {k: calculate_score(word_emb_output[k], keywords_aggregated[k]) for k in list(word_emb_output.keys())}

                #print(synonyms)
                node.synonyms = synonyms

            except KeyError:
                continue
            finally:
                i += 2


    @staticmethod
    def build_keywords_from_links(tree, keyword_file):

        scraper = Scraper()

        # change this to file output
        for entry in  tree.map.keys():
            # print(entry)
            if len(entry) == 0:
                continue

            curr = tree.map.get(entry)

            if curr._visited:
                #print("already visited")
                continue

            if curr.links == []:
                #print("no links")
                continue

            links = curr.links


            resp = {}
            counter = 0
            links_keywords_cache = {}


            for link in links:
                if counter > 20:
                    break
                #print('Trying: ', link)
                link = link.replace('\'', '')
                tdict = None
                try:
                    tdict=links_keywords_cache[link]
                except KeyError:
                    tdict = scraper.get_keywords(link)
                    links_keywords_cache[link] = tdict

            if len(str(tdict)) > 0:
                for key in tdict.keys():
                    try:
                        resp[key].append(tdict[key])
                    except KeyError:
                        resp[key] = [tdict[key]]
                counter+= 1

            #print("writing to file")
            writer = open(keyword_file,'a')
            writer.write(entry + '\n')
            writer.write(str(resp)+'\n')

    @staticmethod
    def build(tree, tags_file, search_links_file, keyword_file):
        TreeBuilder.build_tree_from_tags(tree, tags_file)
        TreeBuilder.build_links_from_file(tree, search_links_file)
        TreeBuilder.build_synonyms_from_file(tree, keyword_file)


def main():
    t = Tree()
    TreeBuilder.build(t, "../resources/tags.txt",
    "../resources/search_links.txt",
    "../resources/keyword_file.txt")

    # TreeBuilder.build_tree_from_tags(t, "/home/sukhad/Workspace/GithHub/contextual-ads/old-code/ConceptHierarchyVisualizer/tags.txt")
    # TreeBuilder.build_links_from_file(t, "/home/sukhad/Workspace/GithHub/contextual-ads/old-code/ConceptHierarchyVisualizer/search_links.txt")
    # TreeBuilder.build_synonyms_from_file(t, "/home/sukhad/Workspace/GithHub/contextual-ads/old-code/Synonym_Builder/keyword_file_formatted")

    t.bfs()
    print(t.map["Boys"].links)
    print(t.map["Boys"].synonyms)

if __name__ == '__main__':
    main()
