# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from items import ScrapemanItem
import datetime
def clean_item(item):
    for k, v in item.items():
        if v is None or v == u'""':
            item[k] = u''

class ScrapemanPipeline(object):
    def open_spider(self, spider):
        self.file = open('sellerlinks-'+str(datetime.date.today())+'.csv','w')

    def close_spider(self, spider):
        spider.driver.close()
        self.file.close()

    def process_item(self, item, spider):
        clean_item(item)
        self.file.writelines(["%s\n" % l for l in item['stores_urls']])
        return item
