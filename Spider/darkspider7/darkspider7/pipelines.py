# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import logging
from datetime import datetime
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class darkspider7Pipeline(object):
    def __init__(self):
        self.file = open("item.txt", "a", encoding="utf-8")


    def process_item(self, item, spider):

        item["create_time"] = datetime.utcnow()    #时间戳
        self.file.write(str(item) + "\r\n")
        self.file.flush()
        print(item)
        return item

    def __del__(self):
        self.file.close()

#下载图片 ImagesPipeline
class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        try:
            image_url = item['image_url']
            yield Request(image_url, meta={'item': item})
        except:
            pass

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    #重写ImagesPipeline中file_path方法
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]  # 取原url的图片命名
        return 'full/%s' % (image_guid)
