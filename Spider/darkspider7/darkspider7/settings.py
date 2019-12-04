# -*- coding: utf-8 -*-

# Scrapy settings for darkspider7 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from datetime import datetime

BOT_NAME = 'darkspider7'

SPIDER_MODULES = ['darkspider7.spiders']
NEWSPIDER_MODULE = 'darkspider7.spiders'

ROBOTSTXT_OBEY = False

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 使用scrapy_redis 里的去重组件，不使用scrapy默认的去重方式
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用scrapy_redis 里的调度器组件，不使用默认的调度器
SCHEDULER_PERSIST = True    # 允许暂停，redis请求记录不丢失

#使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# # 种子队列的信息
REDIS_HOST = '192.168.126.91'    # 连接本机
REDIS_PORT = '6379'   # 端口
# REDIS_PARAMS = {
#     # 'password': '',
#     'db': 1
# }   # 密码一般不设置，使用数据0

# # 去重队列的信息
# FILTER_URL = None
# FILTER_HOST = 'localhost'
# FILTER_PORT = 6379
# FILTER_DB = 0

ITEM_PIPELINES = {
    # 'darkspider7.pipelines.darkspider7Pipeline': 300,
    # 'darkspider7.pipelines.DownloadImagesPipeline': 1,
    'scrapy_redis.pipelines.RedisPipeline': 200,

}
MEDIA_ALLOW_REDIRECTS = True    #因为图片地址会被重定向，所以这个属性要为True
IMAGES_STORE =  './imgs'       #图片下载路径

# 配置UA
USER_AGENT = ''

#请求头
DEFAULT_REQUEST_HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Cache-Control':'max-age=0',
'Host': '35nwli65sok6lnqhn',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests': 1 ,
'Referer':'http://35nwli65sok6lnqh.onion/shop',

}

COOKIES_ENABLED = True      #开启并使用自定义cookie中间件
# COOKIES_DEBUG =True        #跟踪cookiess

LOG_ENABLED = True      #开启日志
LOG_ENCODING = 'utf-8'  #日志字节码
LOG_LEVEL = 'DEBUG'   #日志级别
today = datetime.now()
log_file_path = "log/spiders-{}-{}-{}.log".format(today.year, today.month, today.day)
LOG_FILE = log_file_path    #日志保存为文件
LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'# 日志格式
LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'# 日志时间格式


USER_AGENT_TYPE = 'random'   #fake_useragent
#下载器中间件
DOWNLOADER_MIDDLEWARES = {  'darkspider7.middlewares.IpProxyDownloadMiddleware': 300,
                            'darkspider7.middlewares.RandomUserAgentMiddleware':543,
                            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                            'darkspider7.middlewares.CookieMiddleware': 400,
                            }
#爬虫中间件
#SPIDER_MIDDLEWARES = {
#    'AWS.middlewares.AwsSpiderMiddleware': 543,
#}
# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 5  #下载延时

# 初始下载延迟
#AUTOTHROTTLE_START_DELAY = 5

# 在高延迟情况下设置的最大下载延迟
AUTOTHROTTLE_MAX_DELAY = 60

#使用RetryMiddleware中间件
RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 502, 503, 403, 404, ]    #遇到这些状态码时候重新请求

# Scrapy downloader设置最大并发数（默认是16个，可以自己设置更多。但是要注意电脑的性能）
#CONCURRENT_REQUESTS = 32

# 对单个网站进行并发请求的最大值。
#CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 对单个IP进行并发请求的最大值。如果非0,则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定,使用该设定。 也就是说,并发限制将针对IP,而不是网站。该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0,下载延迟应用在IP而不是网站上
#CONCURRENT_REQUESTS_PER_IP = 16