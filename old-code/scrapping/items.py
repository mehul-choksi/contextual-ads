# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    tags = scrapy.Field()
    product_url = scrapy.Field()
    image_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
