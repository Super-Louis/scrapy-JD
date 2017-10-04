# -*- coding: utf-8 -*-

# Scrapy settings for JD project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import random
BOT_NAME = 'JD'

SPIDER_MODULES = ['JD.spiders']
NEWSPIDER_MODULE = 'JD.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'JD (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:

DEFAULT_REQUEST_HEADERS = {
		'cache-control':'no-cache',
      	'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		'referer':'https://list.jd.com/list.html',
		'cookie':'TrackID=19blJPNAMy9IZ6uZD45obrfQCL8shz225pBx82yXjPmtEReUnEXVQWmJ9ht4ejKGKXniSX_u8x4mgiYLd3_RQ_zGSXqxkNYV-r14ajOdAhkKqZocVPzSetohDOiOswX60; pinId=NeqIDosPOyzrcoIviREEErV9-x-f3wj7; unpl=V2_ZzNtbRACEBZwCxVdfU1YBWIBFFURUEQdcQ8TU3kRWAVnB0FbclRCFXMUR1xnGFQUZwUZWUdcRxZFCEdkeRpbAGcKF1lDZ3MURQtGZHMpXAFhBhBUS1VCEkU4T11LKR9dNVpGHkNXQiVwAEBUehhcAmAzE21KVEQTfQ9EUH4pF2tmThJZRFJBHHwKR1NLGGwG; __jdv=122270672|jcad.c-psa.net|t_326418450_|uniongoubiao|cdb242b87e514379b66956d6395115b7|1504950893802; ipLoc-djd=1-72-4137-0; areaId=1; __jda=122270672.1574388306.1504950891.1505093223.1505117715.5; __jdb=122270672.3.1574388306|5.1505117715; __jdc=122270672; __jdu=1574388306; 3AB9D23F7A4B3C9B=YCOJ4PP323YLTDHQWD5SRUZSPVUROSKTDPG6JRTSGSXA3RAGFXXLZYCD4XLEYTGM7YTBQ4S5VHXX7HB7H5PX64II3U'
		}


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'JD.middlewares.JdSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html

##如果要禁止某一默认的中间件，需将默认中间件设置为None，然后在其中加入自制的中间件
DOWNLOADER_MIDDLEWARES = {
#   'JD.middlewares.MyCustomDownloaderMiddleware': 543,
 # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,  
 # 'JD.middlewares.ProxyMiddleware':125, 
	# 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':550 
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'JD.pipelines.JDPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

