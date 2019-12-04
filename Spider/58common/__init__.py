#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-05 11:12
# @Author  : tang
# @File    : __init__.py.py
# @Software: PyCharm
import urllib2
from BeautifulSoup import BeautifulSoup


get​url='http://jianli.58.com/resume/91655325401100'
content = urllib2.urlopen(url).read()
soup=BeautifulSoup(content)
print soup
