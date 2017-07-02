import scrapy
from items import ScrapemanItem
from selenium import webdriver
import os
from pyvirtualdisplay import Display
from scrapy import Selector



display = Display(visible=0, size=(800, 600))
display.start()


def clean_item(item):
    for k, v in item.items():
        if v is None:
            item[k] = u''


class QuotesSpider(scrapy.Spider):
    name = "spidy"

    def __init__(self):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        urls = ['https://www.google.com/search?q=23100107721',
            'https://www.google.com/search?q=41693392140',
            'https://www.google.com/search?q=49694260437',
            'https://www.google.com/search?q=641265232685',
            'https://www.google.com/search?q=797801035316',
            'https://www.google.com/search?q=14633149517',
            'https://www.google.com/search?q=20626716192',
            'https://www.google.com/search?q=45557180034',
            'https://www.google.com/search?q=43917231709'
            ]
        for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_contents)


    def parse_contents(self, response):
        self.driver.get(response.url)
        print('Scraping URL: %s' % self.url)
        source = self.driver.page_source
        sel = Selector(text=source)
        rows = sel.css('._Dw')
        item = ScrapemanItem()
        item['Url'] = unicode(response.url)
        for idx, select in enumerate(rows):
            item['Store' + str(idx + 1)] = select.css('a > .rhsg4').xpath('text()').extract_first()
            item['Price' + str(idx + 1)] = select.css('._kh').xpath('text()').extract_first().strip(u'$')
            item['Extras' + str(idx + 1)] = "\"" + select.css('._ree').xpath('normalize-space(string())').extract_first() +"\"".encode('utf-8')
            item['id'] = u''
            item['Cost'] = u''
        yield item
