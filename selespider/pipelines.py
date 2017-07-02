# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from items import ScrapemanItem
# import datetime

class ScrapemanPipeline(object):
    def clean_item(item):
        for k, v in item.items():
            if v is None:
                item[k] = u''

    def close_spider(self, spider):

        self.driver.close()

    def process_item(self, item, spider):
        self.clean_item(item)
        return item
