#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-05 11:24
# @Author  : tang
# @File    : Beautisoup.py
# @Software: PyCharm

import urllib2
from BeautifulSoup import BeautifulSoup


strurl = "http://jianli.58.com/resume/91655325401100"
content = urllib2.urlopen(strurl).read()
soup = BeautifulSoup(content)
print soup
data = soup.findAll('li', attrs={'class': 'item'})
print data

