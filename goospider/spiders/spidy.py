import scrapy
from goospider.items import GoospiderItem
import json
from scrapy.http.headers import Headers

RENDER_HTML_URL = "http://127.0.0.1:8050/render.html"

class QuotesSpider(scrapy.Spider):
    name = "spidy"
    handle_httpstatus_list = [302,404]
    urls = ['https://www.amazon.com/gp/offer-listing/B0000C6E0P/ref=dp_olp_new_mbc?ie=UTF8&condition=new']

    def start_requests(self):
        for url in self.urls:
            body = json.dumps({"url": url, "wait": 0.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(url=RENDER_HTML_URL, callback=self.parse_contents, method="POST",
                                 body=body, headers=headers)


    def parse_contents(self, response):
        item = GoospiderItem()
        item['url'] = response.url
        item['price'] = response.css('.a-column.a-span2.olpPriceColumn > .a-color-price').xpath(
            'normalize-space(string())').extract()
        item['condition'] = response.css('.olpCondition').xpath('normalize-space(string())').extract()
        item['delivery'] = response.css('.olpFastTrack > li:first-child').xpath('normalize-space(string())').extract()
        item['sellername'] = response.css('.olpSellerName > span > a, .olpSellerName img').xpath(
            'text()|@alt').extract()
        item['sellerurls'] = ['www.amazon.com' + url for url in response.css('.olpSellerName > span > a').xpath(
            '@href').extract()]

        yield item
