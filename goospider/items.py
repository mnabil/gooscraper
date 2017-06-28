# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    condition = scrapy.Field()
    delivery = scrapy.Field()
    sellername = scrapy.Field()
    sellerurls = scrapy.Field()
