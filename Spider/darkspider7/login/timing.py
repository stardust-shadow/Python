# -*- coding: utf-8 -*-
from login.login7 import *
import schedule
import time


def job1():
    print('开启定时任务:')
    testspider = Spider()
    testspider.login_url()
    testspider.mains()
    testspider.main()


def run():
    schedule.every(150).seconds.do(job1)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()