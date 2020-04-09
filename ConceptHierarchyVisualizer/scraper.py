from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, FancyURLopener
from bs4.element import Comment
from Textrank import TextRank
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import traceback

from random import randint
from time import sleep



class URLOpener(FancyURLopener):
    version = "Mozilla/5.0"

class Scraper():

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='/home/sukhad/Downloads/geckodriver')

    def _tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def get_keywords(self, site):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self._tag_visible, texts)
        obj = TextRank()
        parsed_text=obj.read(u" ".join(t.strip() for t in visible_texts))
        obj.analyze(parsed_text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
        keyword_dict = obj.get_keywords(10)
        for key, val in keyword_dict.items():
            val=round(val,2)
            keyword_dict[key]=val
        return keyword_dict

    def get_search_results_links(self, query="", start=0, resp_links=[]):
        """
            Take a query > search on google > fetch links of search results
        """

        if start>20:
            return resp_links

        sleep(randint(2,10))


        query = query.replace(" ","+")
        site = 'https://www.google.co.in/search?q={query}&start={start}'.format(query=query,start=start)
        self.driver.get(site)

        html = self.driver.page_source
        tval = html
        list_1 = tval.split("<div class=\"r\"><a href=\"")

        n = len(list_1)
        for i in range(1,n):
            curr = list_1[i]
            curr = curr.split("ping")[0]
            curr = curr.split("onmousedown")[0]
            curr = curr.split("\"")[0]
            resp_links.append(curr)

        self.get_search_results_links(query, start+10, resp_links=resp_links)
        self.get_search_results_links(query, start+20, resp_links=resp_links)

        return resp_links

    def __del__(self):
        self.driver.close()



# def scrape(query):
#         sleep(randint(10,100))
#         query = query.replace(" ","+")
#         site = 'https://www.google.co.in/search?q={query}'.format(query=query)
#         driver.get(site)
#
#         html = driver.page_source
#     	tval = html
#
#     	list_1 = tval.split("<div class=\"r\"><a href=\"")
#
#     	n = len(list_1)
#     	resp_links = []
#     	for i in range(1,n):
#
#     		curr = list_1[i]
#     		curr = curr.split("ping")[0]
#
#     		curr = curr.split("onmousedown")[0]
#     		resp_links.append(curr)
#
#
#
# 	return resp_links

# def scrape(query, site=None, resp_links=[]):
#     sleep(randint(2,10))
#
#     if not site:
#         driver.get(site)
#     else:
#         query = query.replace(" ","+")
#         site = 'https://www.google.co.in/search?q={query}'.format(query=query)
#         driver.get(site)
#
#     html = driver.page_source
#     tval = html
#     list_1 = tval.split("<div class=\"r\"><a href=\"")
#
#     n = len(list_1)
#     for i in range(1,n):
#         curr = list_1[i]
#         curr = curr.split("ping")[0]
#         curr = curr.split("onmousedown")[0]
#         resp_links.append(curr)
#
#     return resp_links
#
#
#



if __name__ == "__main__":
    scraper = Scraper()
    links = scraper.get_search_results_links("Girls shirts blogs")
    del scraper

    scraper = Scraper()
    links_2 = scraper.get_search_results_links("Girls shirts blogs")

    print(links)
