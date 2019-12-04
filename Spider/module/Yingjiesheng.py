# -*- coding: utf-8 -*
from Bequest import Bequest


class Yingjiesheng(Bequest):
    def __init__(self, url):
        Bequest.__init__(self, url)

    def parseargs(self):
        doc = self.getpager()
        general_info = doc('.tr_list').items()
        print general_info
        title, link, date, source = ([], [], [], [])
        for g in general_info:
            title.append(g('a').text())
            link.append('http://www.yingjiesheng.com'+g('a').attr('href'))
            date.append(g('.date center').text())
            source.append(g('.cols2').text())
        data = [title, link, date, source]
        self.save2csv(data)
        return title, link, date, source

    def parsedetail(self, link):
        pass

'''
对于北大BBS上的信息我们采用相同的方法，确实通过类的方法只需要把关注点放在对于特定网站的提取上，
基于类有一个更大的优点是对于某个网站来说即使请求头的要求不同，也只需要在该子类中重写它的请求属性而不会对其他的类产生影响。
'''


class PkuBbs(Bequest):
    def __init__(self, url):
        Bequest.__init__(self, url)

    def parsefile(self):
        doc = self.getpager()
        general_info = doc('html body div#page-content div#page-thread.page-thread div#board-body div#list-body.fw '
                           'div#list-content.fw div.list-item-topic.list-item').items()
        title, link, date, source = ([], [], [], [])
        for g in general_info:
            title.append(g(' div.title-cont.l div.title.l.limit').text())
            link.append('https://bbs.pku.edu.cn/v2/' + g('a').attr('href'))
            date.append(g(' div.author.l .time').text())
            source.append('北大未名')
        data = [title, link, date, source]
        self.save2csv(data)
        return title, link, date, source

    def parsedetail(self, link):
        pass
