from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re

nlp = spacy.load('en_core_web_sm')


class TextRank():
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight

    def set_stopwords(self, stopwords):
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True

    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

        return g_norm

    def get_keywords(self, number=10):
        """Print top number keywords"""
        keyword_dict = {}
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            # print(key + ' - ' + str(value))
            keyword_dict[key] = value
            if i > number:
                break
        return keyword_dict

    def analyze(self, text,
                candidate_pos=['NOUN', 'PROPN'],
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""

        # Set stop words
        self.set_stopwords(stopwords)

        # Pare text by spaCy
        doc = nlp(text)

        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower)  # list of list of words

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight

    def read(self, text):
        # reader = open(path + file_name)
        # text = reader.read()
        # remove non alphabetical characters
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = text.lower();
        # remove tags
        text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)
        return text



tr4w = TextRank()
'''path = 'https://pinchofyum.com/the-best-chicken-tinga-tacos'
reader = open(path, 'r')
text = reader.read()'''

text = '''
Accessibility links
Skip to main content
Accessibility help
Accessibility feedback
Google
About 3,54,00,000 results (0.79 seconds) 
Search Results
Web results

Online Shopping at Max
www.maxfashion.in › department › maxboys
Tees & Polos. Shop Now. Tees & Polos · Bottoms. Shop Now. Bottoms · Shirts. Shop Now. Shirts · Essentials. Shop Now. Essentials · Footwear & Accessories.

Sportswear - Max
www.maxfashion.in › Home › Women › Sportswear
Shopping Latest Collection of Sports Wear, Gymwear, Workout Outfits, Dresses & Clothes Online For Ladies at MaxFashion|✓Free Shipping* ✓Easy Return ...

Sportswear - Girls: Clothing & Accessories ... - Amazon.in
www.amazon.in › ...
Online shopping for Clothing & Accessories from a great selection of Trousers, Shirts & Tees, Shorts, Innerwear, Tights & Leggings, Athletic Socks & more at ...
Missing: blogs ‎| Must include: blogs

View all
More images for Clothing & Accessories Girls Sportswear Shirts & Tees blogs
Report images
Web results

Sportswear - Wikipedia
en.wikipedia.org › wiki › Sportswear
Sportswear or activewear is clothing, including footwear, worn for sport or physical exercise. Sport-specific clothing is worn for most sports and physical exercise, for practical, comfort or safety reasons. Typical sport-specific garments include tracksuits, shorts, T-shirts and polo ... While generally women players of indoor volleyball wear T-shirt and shorts, ...

American Apparel: Your AA
americanapparel.com
Effortless basics and iconic fashion favorites for women, men and kids. The original basic, from tees to hoodies, denim and more.

Pantaloons Official Online Store - Lightning Deals Like Never ...
www.pantaloons.com
Grab our #StyleYourChange Deals on Women's Clothing, Men's Clothing & Kids Clothing with Free Alterations/Exchange - Your Pantaloons Online Apparel ...

Customized Girl - Custom Shirts, Tanks, Undies, & More
www.customizedgirl.com
Use our design center to add your own text, art, and images to personalized apparel & accessories. Tees, Sweatshirts, Bags, & more!

Roxy | Surf, Snowboard & Fitness Brand - Women's Lifestyle
www.roxy.com
New · Clothing · Swim · Accessories · Shoes · Fitness · Surf · Snow · Kids · Sale. If you love to embrace the world of possibilities each day has to offer, and seek ...

Clothing Sale: Women's and Men's Clearance Clothing ...
www.forever21.com › ... › Promotion › Sale Left Nav
Get up to 70% off men's and women's clothing & accessories. ... both wardrobe basics like sweatshirts and denim, as well as jackets, activewear, and beauty picks. ... Give it a go and pick up your favorite band, music artists, and television characters all on a t-shirt. ... As for Girls, pick up a new outfit she can show off at school!
Searches related to Clothing & Accessories Girls Sportswear Shirts & Tees blogs

sports wear for girls

gym wear for ladies

women's gym wear cheap

ladies gym wear wholesale

zivame gym wear

sportswear near me

sports wear for men

gym wear shop near me
Page navigation
	
Next
Footer links
India411028, Pune, Maharashtra - From your Internet address - Use precise location - Learn more
HelpSend feedbackPrivacyTerms

'''
#remove non alphabetical characters
text = re.sub('[^a-zA-Z]', ' ', text)
text = text.lower();
#remove tags
text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
# remove special characters and digits
text=re.sub("(\\d|\\W)+"," ",text)

tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
print(tr4w.get_keywords(20))

