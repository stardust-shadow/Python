# -*- coding: utf-8 -*-
import logging
from scrapy import Request
from scrapy_redis.spiders import RedisSpider


class SpidersSpider(RedisSpider):
    name = 'spiders'
    # allowed_domains = ['tochka3evlj3sxdv.onion/marketplace']
    # start_urls = ['http://tochka3evlj3sxdv.onion/marketplace/']x
    redis_key = "spiders:start_url"

    def parse(self, response):
        print(response.status)
        item = dict()
        list_urls = response.xpath('//div[@class="ui menu tiny horizontal ten item top-menu inverted stackable"]/a/@href').extract()
        for list_url in list_urls[2:4]:
            list_url = response.urljoin(list_url)
            # 列表页url
            item['list_url'] = list_url
            logging.info(list_url)
            yield Request(list_url, callback=self.parse_sencond, meta={'item': item})

    # 翻页
    def parse_sencond(self, response):
        print(response.status)
        item = response.meta['item']
        try:
            next_pages = response.xpath('//div[@class="thirteen wide column"]/div[4]/div/a/@href').extract()
            for next_page in next_pages:
                if next_page != " javascript:;":
                    #next_page = 'http://tochka3evlj3sxdv.onion/marketplace/'+str(next_page)
                    next_page = response.urljoin(next_page)
                    logging.info(next_page)
                    yield Request(next_page, callback=self.parse_third, meta={'item': item})
        except:
            pass
    def parse_third(self,response):
        item = response.meta['item']
        details_urls = response.xpath(
            '//div[@class="ui grid stackable"]/div[@class="four wide column"]/div/div[1]/a/@href').extract()
        for url in details_urls:
            url = response.urljoin(url)
            item['url'] = url  # 详情页url
            logging.info(url)
            yield Request(url, callback=self.parse_fourth, meta={'item': item})

    def parse_fourth(self,response):
        item = response.meta['item']
        html = response.body  # 详情页html源文件
        html = str(html, encoding='utf-8')
        # logger.info(html)
        item['html'] = html
        # try:
        #     about = response.xpath('//div[@class="ui segment"][1]/div/p/text()').extract()
        #     logger.error(about)
        # except:
        #     about = ''
        # try:
        #     reviews = response.xpath('//div[@class="ui menu pointing secondary four item"]/a[2]/span/text()').extract()
        #     logger.error(reviews)
        # except:
        #     reviews = ''
        yield item
