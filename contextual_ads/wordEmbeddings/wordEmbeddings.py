import collections
import numpy
from scipy import spatial

class Embeddings:
    def __init__(self):
        self.path = PATH = "/home/sukhad/Workspace/Machine_learning/Embeddings/GloVe/glove.6B.100d.txt"
        self.embeddings_dict = dict()

        with open(self.path,'r') as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = numpy.asarray(values[1:], "float32")
                self.embeddings_dict[word] = vector


    def find_relevant_keywords(self, first_list, second_list, num=20):
        _relevant_words = dict()
        for word2 in second_list:
            score_list = list()
            for word1 in first_list:
                try:
                    score_list.append(1 - spatial.distance.cosine(self.embeddings_dict[word1.lower()], self.embeddings_dict[word2.lower()]))
                except:
                    continue
            if not len(score_list)==0:
                _relevant_words[word2] = max(score_list)
        return dict(collections.Counter(_relevant_words).most_common(num))
