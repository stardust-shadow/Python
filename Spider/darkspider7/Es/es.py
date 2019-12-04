# -*- coding: utf-8 -*-
import json
import logging
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from redis import StrictRedis

logger = logging.getLogger(__name__)   #日志
logger.setLevel(level=logging.INFO)   #日志级别
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') #日志时间、执行程序路径、日志当前行号、日志级别、日志信息
sh = logging.StreamHandler()  # 往屏幕上输出
sh.setFormatter(formatter)  # 设置屏幕上显示的格式
today = datetime.now()
log_file_path = "../log/es-{}-{}-{}.log".format(today.year, today.month, today.day)
handler = logging.FileHandler(log_file_path,encoding='utf-8')     #往文件输出
handler.setFormatter(formatter)     #设置文件写入格式
logger.addHandler(handler)        #把对象加入到logger里
logger.addHandler(sh)

#从redis数据库中读取数据
client = StrictRedis(host='192.168.126.91', port=6379,db=0)
#连接Elasticsearch
es = Elasticsearch(hosts='192.168.126.90', port=9200)

#创建es表
def create_index():
    mappings = {
        "mappings": {
        "abcd":{
        "properties": {
        "url": {"type": "keyword"},
        "html": {"type": "text"},
        "domain_name": {"type": "keyword"},
        "language": {"type": "keyword"},
        "crawl_time": {"type": "date"}
        }
    }
  }
}
    try:
        res = es.indices.create(index='darkspider7', body=mappings)
        logger.info(res)
        logger.info('创建表成功')
        write_index()
    except:
        logger.info('表已存在')
        write_index()

#批量写入数据
def write_index():
    while True:
        start_time = time.time()
        time.sleep(2)
        source, data = client.blpop(["spiders:items"])
        data = json.loads(data.decode("utf-8"))
        list = []
        list.append(data)
        # start_html = data["start_html"]
        # list_html = data["list_html"]
        index_name = 'darkspider7'
        index_type = 'abcd'
        actions = []
        i = 1
        for line in list:
            logger.info(line['url'])
            logger.info(line['html'])
            action = {
                "_index": index_name,
                "_type": index_type,
                "_id": i, #_id 也可以默认生成，不赋值
                "_source": {
                    "url": line['url'],
                    "html": line['html'],
                    "domain_name": 'http://tochka3evlj3sxdv.onion/',
                    "language": 'English',
                    "crawl_time": datetime.utcnow(),
                }
      }
            i += 1
            actions.append(action)
            success, _ = bulk(es, actions, index=index_name, raise_on_error=True)
            end_time = time.time()
            logger.info(end_time-start_time)

# def run():
#     po = Pool(3)  # 最大的进程数为3
#     for i in range(0, 6):
#         '''每次循环将会用空闲出来的子进程去调用目标'''
#         po.apply_async(write_index,(i,))
#
#     print("----start----")
#     po.close()  # 关闭进程池，关闭后po不再接受新的请求
#     po.join()  # 等待po中的所有子进程执行完成，必须放在close语句之后
#     print("-----end-----")

#查看表
# def look():
#     result = es.search(index="maket")
#     print(result)


if __name__ == '__main__':
    create_index()
    # write_index()
    # logger.warning('es读取存储成功')
    # look()