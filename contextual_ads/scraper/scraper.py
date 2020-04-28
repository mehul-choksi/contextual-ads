from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, FancyURLopener
from bs4.element import Comment
from textRank.textRank import TextRank
from pprint import pprint

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

import traceback

from random import randint
from time import sleep

import requests


class URLOpener(FancyURLopener):
    version = "Mozilla/5.0"

class Scraper():

    def __init__(self):
        pass
        #profile = webdriver.FirefoxProfile()
        #profile.set_preference("general.useragent.override","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0")
        #self.driver = webdriver.Firefox(profile,executable_path='/home/ash/workspace/mehul/contextual_ads/scrapping/geckodriver')


    def _tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def get_keywords(self, site):
        try:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site, headers=hdr)
            page = urlopen(req,timeout=10).read()
        except:
                return {}

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


'''
    def get_search_results_links(self, query="", start=0, resp_links=[]):

            #Take a query > search on google > fetch links of search results


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

    #def __del__(self):
    #    self.driver.close()


if __name__ == "__main__":
    scraper = Scraper()
    links = scraper.get_search_results_links("Girls shirts blogs")
    del scraper

    scraper = Scraper()
    links_2 = scraper.get_search_results_links("Girls shirts blogs")

    print(links)
'''
