# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import random
import pymysql
from settings import USER_AGENT_TYPE
from fake_useragent import UserAgent  #引用fake_useragent库
import json
from scrapy.downloadermiddlewares.retry import RetryMiddleware

# 代理中间件


class IpProxyDownloadMiddleware(object):
    PROXIES = [
               '192.168.126.110:9008',
               '192.168.126.107:9398',
               '192.168.126.106:9398',
               '192.168.126.105:9398',
               '192.168.126.108:9398',
    ]

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = 'http://' + proxy
        #logger.info('代理应用成功')
    # def process_response(self, request, response, spider):
    #     if response.status == 403:
    #         return request
    #     else:
    #         return response
#UA中间件
class RandomUserAgentMiddleware(object):
    # 随机更换User-Agent
    def __init__(self):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = USER_AGENT_TYPE  # 在settings中配置指定的ua类型：USER_AGETN_TYPE = 'chrome'，任何想要的类型都可以，也可以是随机类型random
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        if get_ua():
            request.headers.setdefault('User-Agent', get_ua())

# 自定义cookie中间件


class CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    # 从数据库获取cookie

    def get_cookie_mysql(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database="darkspider7")  # 连接mysql数据库
        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT cookies FROM data where id=1")
        cookies = cursor.fetchone()[0]          # fetchall是在两个嵌套元组里fetchone在一个元组里
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        cookies_dict = dict()
        for cookie in listcookies:
            cookies_dict[cookie['name']] = cookie['value']
            # print(cookies_dict)
            # print(type(cookies_dict))
            #logger.info("获取Cookie成功！")
        return cookies_dict

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    # 判断cookie是否失效
    def process_response(self, request, response, spider):
        # 想要拦截重定向需要在settings中进行配置
        if response.status == 403 :
            logging.warning("当出现403时重新获取cookie")
            request.cookies = self.get_cookie_mysql()
            # 返回当前的请求重新加入爬取队列
            return request
        else:
            return response


class Awc3SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Awc3DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
