from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from bs4.element import Comment
from Textrank import TextRank

class Scraper():

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def keywords(self, site):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        obj = TextRank()
        parsed_text=obj.read(u" ".join(t.strip() for t in visible_texts))
        obj.analyze(parsed_text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
        keyword_dict = obj.get_keywords(10)
        for key, val in keyword_dict.items():
            val=round(val,2)
            keyword_dict[key]=val
        return keyword_dict

# obj=Scraper()
# obj.keywords("https://pinchofyum.com/the-best-chicken-tinga-tacos")
