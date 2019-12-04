#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-24 16:13
# @Author  : tang
# @File    : tor_request.py
# @Software: PyCharm


import requests

my_proxies = {"http": "http://127.0.0.1:9050", "https": "https://127.0.0.1:9050"}
resp = requests.get("http://www.disneypicture.net/data/media/17/Donald_Duck2.gif", proxies=my_proxies, timeout=5)
print(resp.text)
