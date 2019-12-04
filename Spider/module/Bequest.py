# -*- coding: utf-8 -*
import requests
from pyquery import PyQuery as pq
import pandas as pd


# noinspection PyMethodMayBeStatic
class Bequest:
    def __init__(self, url):
        self.url = url
        self.expired = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0'}
        self.begin_date = 1
        # input('请输入需要获取信息的起始日')

    def getpager(self):
        webpage = requests.get(self.url, headers=self.expired)
        webpage.encoding = webpage.apparent_encoding
        doc = pq(webpage.text)
        return doc

    def save2csv(self, data):
        df = pd.DataFrame(data).T
        df.to_csv('Jibing.csv', mode='a', header=False, encoding='utf-8')
