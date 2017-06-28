# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
from twisted.internet.ssl import ClientContextFactory
from OpenSSL import SSL
from twisted.internet._sslverify import ClientTLSOptions

class GoospiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SetDefaultCookiejarMiddleware(object):
    """
    This middleware's whole purpose is to set the cookiejar's value to 0 if it doesn't exit
    """

    def process_request(self, request, spider):
        cookiejar = request.meta.get('cookiejar', 0)
        request.meta.update({'cookiejar': cookiejar})


class CustomClientContextFactory(ScrapyClientContextFactory):
    def getContext(self, hostname=None, port=None):
        ctx = ClientContextFactory.getContext(self)
        # Enable all workarounds to SSL bugs as documented by
        # http://www.openssl.org/docs/ssl/SSL_CTX_set_options.html
        ctx.set_options(SSL.OP_ALL)
        if hostname:
            ClientTLSOptions(hostname, ctx)
        return ctx

# class RandomUserAgentMiddleware(UserAgentMiddleware):
#     def __init__(self, settings, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                                             "Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36"):
#         super(RandomUserAgentMiddleware, self).__init__()
#         self.user_agent = user_agent
#         try:
#             self.user_agent_engine = UserAgent()
#         except Exception, ex:
#             logging.error("Failed to create user agent engine object. Reason: %s", ex)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         obj = cls(crawler.settings)
#         crawler.signals.connect(obj.spider_opened,
#                                 signal=signals.spider_opened)
#         return obj
#
#     def process_request(self, request, spider):
#         try:
#             # Using specific user agent if the merchants have this option.
#             if spider.user_agent:
#                 user_agent = spider.user_agent
#             # Using random user agent to prevent block from merchants.
#             else:
#                 user_agent = self.user_agent_engine.random
#         except Exception, ex:
#             logging.error("Failed to get the automatic user agent. Reason: %s", ex)
#             user_agent = self.user_agent
#         logging.info("[kipp] Using user agent (%s)", user_agent)
#         request.headers.setdefault('User-Agent', user_agent)

# import re
# import random
# import base64
# import logging
#
# log = logging.getLogger('scrapy.proxies')
#
#
# class Mode:
#     RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)
#
#
# class RandomProxy(object):
#     def __init__(self, settings):
#         self.mode = settings.get('PROXY_MODE')
#         self.proxy_list = settings.get('PROXY_LIST')
#         self.chosen_proxy = ''
#         if self.proxy_list is None:
#             raise KeyError('PROXY_LIST setting is missing')
#
#         if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
#             fin = open(self.proxy_list)
#             self.proxies = {}
#             for line in fin.readlines():
#                 parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line.strip())
#                 if not parts:
#                     continue
#
#                 # Cut trailing @
#                 if parts.group(2):
#                     user_pass = parts.group(2)[:-1]
#                 else:
#                     user_pass = ''
#
#                 self.proxies[parts.group(1) + parts.group(3)] = user_pass
#             fin.close()
#             if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
#                 self.chosen_proxy = random.choice(list(self.proxies.keys()))
#         elif self.mode == Mode.SET_CUSTOM_PROXY:
#             custom_proxy = settings.get('CUSTOM_PROXY')
#             self.proxies = {}
#             parts = re.match('(\w+://)(\w+:\w+@)?(.+)', custom_proxy.strip())
#             if not parts:
#                 raise ValueError('CUSTOM_PROXY is not well formatted')
#
#             if parts.group(2):
#                 user_pass = parts.group(2)[:-1]
#             else:
#                 user_pass = ''
#
#             self.proxies[parts.group(1) + parts.group(3)] = user_pass
#             self.chosen_proxy = parts.group(1) + parts.group(3)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def process_request(self, request, spider):
#         # Don't overwrite with a random one (server-side state for IP)
#         if 'proxy' in request.meta:
#             if request.meta["exception"] is False:
#                 return
#         request.meta["exception"] = False
#         if len(self.proxies) == 0:
#             raise ValueError('All proxies are unusable, cannot proceed')
#
#         if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
#             proxy_address = random.choice(list(self.proxies.keys()))
#         else:
#             proxy_address = self.chosen_proxy
#
#         proxy_user_pass = self.proxies[proxy_address]
#
#         if proxy_user_pass:
#             request.meta['proxy'] = proxy_address
#             basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
#             request.headers['Proxy-Authorization'] = basic_auth
#         else:
#             log.debug('Proxy user pass not found')
#         log.debug('Using proxy <%s>, %d proxies left' % (
#                 proxy_address, len(self.proxies)))
#
#     def process_exception(self, request, exception, spider):
#         if 'proxy' not in request.meta:
#             return
#         if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
#             proxy = request.meta['proxy']
#             try:
#                 del self.proxies[proxy]
#             except KeyError:
#                 pass
#             request.meta["exception"] = True
#             if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
#                 self.chosen_proxy = random.choice(list(self.proxies.keys()))
#             log.info('Removing failed proxy <%s>, %d proxies left' % (
#                 proxy, len(self.proxies)))