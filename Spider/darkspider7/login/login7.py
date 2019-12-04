# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from login.chaojiying import *
from login.cookie7 import *

logger = logging.getLogger(__name__)   #日志
logger.setLevel(level=logging.INFO)   #日志级别
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') #日志时间、执行程序路径、日志当前行号、日志级别、日志信息
sh = logging.StreamHandler()  # 往屏幕上输出
sh.setFormatter(formatter)  # 设置屏幕上显示的格式
today = datetime.now()
log_file_path = "../log/login-{}-{}-{}.log".format(today.year, today.month, today.day)
handler = logging.FileHandler(log_file_path,encoding='utf-8')     #往文件输出
handler.setFormatter(formatter)     #设置文件写入格式
logger.addHandler(handler)        #把对象加入到logger里
logger.addHandler(sh)


class Spider(object):
    def __init__(self):
        # self.profile = self.get_profile()     #火狐相关设置
        self.chromeOptions = self.get_profile()
        self.browser = self.get_browser()
        self.wait = self.get_wait()
    def mains(self):
        self.get_count()
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')  # 用户中心>>软件ID 生成一个替换 96001
        im = open('code7.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        # print(chaojiying.PostPic(im, 1902))		            	        #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        code = chaojiying.PostPic(im, 5201)
        global results
        results = code["pic_str"]  # 解析的验证码结果取字典的value
        logger.info(results)
        self.count_res()

    def main(self):
        self.get_image()
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')	#用户中心>>软件ID 生成一个替换 96001
        im = open('code26.png', 'rb').read()							        #本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        # print(chaojiying.PostPic(im, 1902))		            	        #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        code = chaojiying.PostPic(im, 4008)
        global result
        result = code ["pic_str"]                   #解析的验证码结果取字典的value
        logger.info(result)
        self.login()

    def get_profile(self):
        #谷歌相关设置
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')         # 谷歌无头模式
        chromeOptions.add_argument('--disable-gpu')       # 谷歌文档提到需要加上这个属性来规避bug 这是禁用显卡
        chromeOptions.add_argument('window-size=1280,800')  # 指定浏览器分辨率
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--proxy-server=http://192.168.126.110:9008")        # 设置代理
        return chromeOptions

    def get_browser(self):
        #谷歌相关设置
        browser = webdriver.Chrome(chrome_options=self.chromeOptions)
        #browser.set_window_size(1280,800)
        return browser
    def get_wait(self):
        wait = WebDriverWait(self.browser, 10)     # 强制等待10s
        return wait

    #计算验证码的处理
    def count_res(self):
        try:
            self.browser.find_element_by_xpath(
                '/html/body/div/div[2]/div/div/form/div[1]/div[1]/input').send_keys(results)  # 账号输入
        except:
            print("第一个验证码输入有误")
        try:
            button = self.browser.find_element_by_xpath('/html/body/div/div[2]/div/div/form/button')
            button.click()
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.required:nth-child(7) > div:nth-child(2) > input:nth-child(1)')))
            logger.info('第一个验证码计算成功并输入')
        except:
            self.mains()
            logger.info('回调1')

    #普通登录验证码处理
    def login(self):
        try:
            self.browser.find_element_by_xpath(
                '/html/body/div/div[2]/div/div/form/div[1]/div/input').send_keys('wahaha')       #账号输入
        except:
            print("账号输入有误")
        try:
            self.browser.find_element_by_xpath(
                '/html/body/div/div[2]/div/div/form/div[3]/input').send_keys('laoganma')     #密码输入
        except:
            print("密码输入有误")
        try:
            self.browser.find_element_by_xpath\
                ('/html/body/div/div[2]/div/div/form/div[5]/div[1]/input').send_keys(result)        #输入解析的验证码
            logger.info('第二个验证码输入')
        except:
            logger.warning("验证码输入错误")
        try:
            button = self.browser.find_element_by_xpath('/html/body/div/div[2]/div/div/form/button')
            button.click()        #点击登录按钮
            logger.info('点击登录')
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.red')))
            logger.info('登录成功')
            self.get_cookies()
            self.browser.quit()
        except:
            self.main()
            logger.info('回调2')

    def get_cookies(self):
        cookies = self.browser.get_cookies()
        self.browser.quit() #关闭浏览器
        jsonCookies = json.dumps(cookies)
        # with open('../login/cookies.json', 'w') as f:
        #     f.write(jsonCookies)
        # return jsonCookies
        sql_save()
        sql1_save(jsonCookies)

    def login_url(self):                    #访问目标网址
        try:
            self.browser.get("http://tochka3evlj3sxdv.onion/marketplace")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.ui')))
        except:
            while True:
                self.browser.refresh()    #刷新当前页面,因为可能会因为网络问题造成阻塞
                time.sleep(30)
                if self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.ui'))):
                    break

    def get_count(self):  # 对验证码所在位置进行定位，然后截取验证码图片

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.ui')))
        self.browser.save_screenshot('codes7.png')      # 截取全屏
        imgelement = self.browser.find_element_by_xpath('/html/body/div/div[2]/div/div/form/div[1]/div[2]/img')  # 定位验证码
        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标

        img = Image.open('codes7.png')                     # 打开全屏，进行验证码截取
        im = img.crop(rangle)                               # 将图片的位置作为一个元组传入
        im.save('code7.png')                               # 最后保存图片



    def get_image(self):  # 对验证码所在位置进行定位，然后截取验证码图片

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.ui')))
        self.browser.save_screenshot('codes26.png')      # 截取全屏
        imgelement = self.browser.find_element_by_xpath('/html/body/div/div[2]/div/div/form/div[5]/div[2]/img')  # 定位验证码
        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标

        img = Image.open('codes26.png')                     # 打开全屏，进行验证码截取
        im = img.crop(rangle)                               # 将图片的位置作为一个元组传入
        im.save('code26.png')                               # 最后保存图片




if __name__ == '__main__':
    testspider = Spider()
    testspider.login_url()
    testspider.mains()
    testspider.main()

