# -*- coding: utf-8 -*
from Yingjiesheng import Yingjiesheng
from Yingjiesheng import PkuBbs

purl = 'https://bbs.pku.edu.cn/v2/thread.php?bid=896&mode=topic&page={page}&_pjax=%23page-content'
for p in range(3):
    yingjiesheng = Yingjiesheng('http://www.yingjiesheng.com/beijing-moreptjob-{page}.html'.format(page=p))
    pkubbs = PkuBbs(purl.format(page=p))
    yingjiesheng.parseargs()
    pkubbs.parsefile()
