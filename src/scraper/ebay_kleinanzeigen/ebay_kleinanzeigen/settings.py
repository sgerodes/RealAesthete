from . import proxies
from . import spiders
from . import pipelines
# Scrapy settings for ebay_kleinanzeigen project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


def get_full_package_name_for_class(clazz) -> str:
    return ".".join([clazz.__module__, clazz.__name__])


def get_full_package_name_module(module) -> str:
    return module.__name__


BOT_NAME = 'ebay_kleinanzeigen'

SPIDER_MODULES = [get_full_package_name_module(spiders)]  # ['src.scraper.ebay_kleinanzeigen.ebay_kleinanzeigen.spiders']
NEWSPIDER_MODULE = get_full_package_name_module(spiders)  # 'src.scraper.ebay_kleinanzeigen.ebay_kleinanzeigen.spiders'

ITEM_PIPELINES = {
    get_full_package_name_for_class(pipelines.EbayKleinanzeigenPersistencePipeline): 300
}

# Rotating proxies
#ROTATING_PROXY_LIST = proxies.proxies
# ROTATING_PROXY_LIST_PATH = r'C:\Users\sgero\PycharmProjects\RealAesthete\src\scraper\ebay_kleinanzeigen\ebay_kleinanzeigen\free-proxy-list_net.proxies'
ROTATING_PROXY_LIST_PATH = r'C:\Users\sgero\PycharmProjects\RealAesthete\src\scraper\ebay_kleinanzeigen\ebay_kleinanzeigen\good_proxy.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ebay_kleinanzeigen (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ebay_kleinanzeigen.middlewares.EbayKleinanzeigenSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ebay_kleinanzeigen.middlewares.EbayKleinanzeigenDownloaderMiddleware': 543,
#}
#DOWNLOADER_MIDDLEWARES = {
#    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
