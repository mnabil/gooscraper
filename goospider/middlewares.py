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
from scrapy import Request
import re
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent

class ScrapemanSpiderMiddleware(object):
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

class AdjustSplashUrlMiddleware(object):
    """
    This middlware is located directly after splash downloader middleware
    and its purpose is to replace the url of the response got from splash middleware
    with the rendered page's url.
    """

    def process_response(self, request, response, spider):
        """
            see: http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.DownloaderMiddleware.process_response

            if the request that corresponds to the given response was rendered by splash(contains 'splash' key in its meta)
            then replace the given response's url with target url
        """
        return response.replace(
                url=request.meta['splash']['args']['url']) if '_splash_processed' in request.meta else response

class AddSplashMetaMiddleware(object):
    """
    This middleware is responsible for adding splash meta to requests got from spiders to be rendered by splash
    """

    def _add_splash_meta(self, request, spider):
        """

        :param request: Splash.request to be rendered with splash
        :return: the given request with splash meta added
        """
        splash_args = {'html': 1, 'wait': 0.5}
        if spider.splash_args:
            splash_args.update(spider.splash_args)

        request.meta.update({
            'splash': {
                'args': splash_args,
                'endpoint': 'render.html',
                'dont_process_response': True
            },
        })
        return request

    def _needs_js_rendering(self, spider, request):
        """
        uses render_js_regexes to find if the given request should be rendered by splash
        by trying to match the given request's url agains the regexes defined in the spider
        :param spider: spider
        :param request:
        :return: boolean representing the given request should be rendered by splash
        """
        render_js_regexes = spider.render_js_regexes
        return any(re.search(regex, request.url) for regex in render_js_regexes) if render_js_regexes else True

    def _get_processed_result(self, result, spider):
        if isinstance(result, Request) and self._needs_js_rendering(spider, result):
            result = self._add_splash_meta(result, spider)
        return result

    def process_spider_output(self, response, result, spider):
        return (self._get_processed_result(r, spider) for r in result) if spider.render_js else result

    def process_start_requests(self, start_requests, spider):
        if hasattr(spider, 'render_js'):
            if spider.render_js:
                return (self._get_processed_result(request, spider) for request in start_requests)
        return start_requests

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, settings, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                            "Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36"):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        try:
            self.user_agent_engine = UserAgent()
        except Exception, ex:
            logging.error("Failed to create user agent engine object. Reason: %s", ex)

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        try:
            # Using specific user agent if the merchants have this option.
            if spider.user_agent:
                user_agent = spider.user_agent
            # Using random user agent to prevent block from merchants.
            else:
                user_agent = self.user_agent_engine.random
        except Exception, ex:
            logging.error("Failed to get the automatic user agent. Reason: %s", ex)
            user_agent = self.user_agent
        logging.info("[spidy] Using user agent (%s)", user_agent)
        request.headers.setdefault('User-Agent', user_agent)
