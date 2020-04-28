import scrapy
from scrapy.selector import Selector
from Webscraping.items import ProductItem
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from treelib import Tree


class BestSellerSpider(scrapy.Spider):
    name = "Scraper"
    headers = {
        'User-Agent': 'Mozilla/4.1 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 100
    }
    tree = Tree()
    tree.create_node("Category", "Any Department")
    prodlist = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dispatcher.connect(self.quit, signals.spider_closed)

    def start_requests(self):
        search_query = "https://www.amazon.in/gp/bestsellers"
        urls = [search_query]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        namelist = []
        linklist = []
        item = Selector(response=response).xpath('//ul[@id="zg_browseRoot"]//ul')
        flag = True
        while flag:
            temp = item.xpath('.//ul')
            if len(temp.extract()) == 0:
                flag = False
            else:
                item = temp

        for cat in item.xpath('li'):
            selected = cat.xpath('span[@class="zg_selected"]')
            if len(selected.extract()) != 0:
                catname = selected.xpath('text()').extract()[0]
                parlist = [catname]
                parent = ""
                parpath = cat
                while parent != 'Any Department':
                    parpath = parpath.xpath('../..//li')
                    parent = parpath.xpath("a/text()").extract()
                    if len(parent) == 0:
                        parpath = parpath.xpath('../..//li')
                        parent = parpath.xpath('span[@class="zg_selected"]/text()').extract()
                    parent = parent[0]
                    parent = parent.strip()
                    parlist.append(parent)
                parlist.reverse()
                for i in range(len(parlist) - 1):
                    child = parlist[i + 1]
                    temppar = parlist[i]
                    if self.tree.contains(temppar) and not self.tree.contains(child):
                        self.tree.create_node(child, child, parent=temppar)

                cnt = 0
                for prod in Selector(response=response).xpath(
                        './/ol[@id="zg-ordered-list"]//li//div[@class="p13n-sc-truncate p13n-sc-line-clamp-2"]'):

                    name = prod.xpath('text()').extract()[0]
                    name = name.strip()
                    if name == 'Amazon Pay eGift Card':
                        continue
                    taglist = [catname]
                    par = self.tree.parent(catname)
                    while par is not None and par.tag != "Category":
                        taglist.append(par.tag)
                        par = self.tree.parent(par.identifier)
                    taglist.reverse()
                    imgurl = prod.xpath('..//img/@src').extract()[0]

                    prod_url = "https://www.amazon.in" + prod.xpath('../..//@href').extract()[0]
                    product_item = ProductItem()
                    product_item['name'] = name
                    product_item['tags'] = taglist
                    product_item['image_urls'] = [imgurl]
                    imgname = name.replace("/", "_").replace("\\", "_").replace("|", "_").replace(
                        ":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">",
                                                                                                                  "_")
                    product_item['image_name'] = imgname
                    product_item['product_url'] = prod_url

                    yield product_item
                    self.prodlist.append(product_item)
                    cnt = cnt + 1
                    if cnt >= 2:
                        break

            else:
                catname = cat.xpath('a/text()').extract()[0]
                if catname != "Amazon Launchpad" and catname != "Apps for Android" and catname != "Gift Cards":
                    # parent = cat.xpath('../..//li//span[@class="zg_selected"]/text()').extract()
                    # if len(parent) == 0:
                    #     parent = cat.xpath('../..//li//a/text()').extract()
                    # parent = parent[0]
                    # parent = parent.strip()
                    # if self.tree.contains(parent) and not self.tree.contains(catname):
                    #     self.tree.create_node(catname, catname, parent=parent)
                    linkname = cat.xpath('a/@href').extract()[0]
                    namelist.append(catname)
                    linklist.append(linkname)

                    for url in linklist:
                        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def quit(self, spider):
        print(self.tree.show())
        print(self.prodlist)
