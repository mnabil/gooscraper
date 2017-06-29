# -*- coding: utf-8 -*-

# Scrapy settings for scrapeman project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import datetime
BOT_NAME = 'goospider'

SPIDER_MODULES = ['goospider.spiders']
NEWSPIDER_MODULE = 'goospider.spiders'

DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 302, 301]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scrapeman (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
SPLASH_URL = 'http://localhost:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scrapeman.pipelines.ScrapemanPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# -*- coding: utf-8 -*-

# Scrapy settings for kipp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 2,
    'goospider.middlewares.SetDefaultCookiejarMiddleware': 601,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'goospider.middlewares.AdjustSplashUrlMiddleware': 726,
    'goospider.middlewares.RandomUserAgentMiddleware': 400,
}

SPIDER_MIDDLEWARES = {
    'goospider.middlewares.AddSplashMetaMiddleware': 910,
}

FEED_EXPORTERS = {
    'csv': 'goospider.scrapeman_csv_item_exporter.MyProjectCsvItemExporter',
}

FEED_URI='result-'+str(datetime.date.today())+'.csv'
FEED_FORMAT='csv'

# FIELDS_TO_EXPORT = [
#     'url',
#     'price1',
#     'delivery1',
#     'sellername1',
#     'price2',
#     'delivery2',
#     'sellername2',
#     'price3',
#     'delivery3',
#     'sellername3',
#     'price4',
#     'delivery4',
#     'sellername4',
#     'price5',
#     'delivery5',
#     'sellername5',
#     'price6',
#     'delivery6',
#     'sellername6',
#     'price7',
#     'delivery7',
#     'sellername7',
#     'price8',
#     'delivery8',
#     'sellername8',
#     'price9',
#     'delivery9',
#     'sellername9',
#     'price10',
#     'delivery10',
#     'sellername10']

# ITEM_PIPELINES = {
#     'goospider.pipelines.ScrapemanPipeline': 1
# }
