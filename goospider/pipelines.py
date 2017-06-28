# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from goospider.items import GoospiderItem
# import datetime
#
# class GoospiderPipeline(object):
#     def open_spider(self, spider):
#         self.file = open('sellerlinks-'+str(datetime.date.today())+'.csv','w')
#
#     def close_spider(self, spider):
#         self.file.close()
#
#     def process_item(self, item, spider):
#         self.file.writelines(["%s\n" % l for l in item['sellerurls']])
#         data_fields = [i for i in item.iterkeys() if i != 'url' and i != 'condition' and i !='sellerurls']
#         data = {}
#         data['url'] = item['url']
#         for field in data_fields:
#             for idx, value in enumerate(item[field]):
#                 data[field + str(idx + 1)] = value
#         return data
