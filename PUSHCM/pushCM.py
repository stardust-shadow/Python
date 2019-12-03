# -*- coding=utf-8 -*-
import http.cookiejar
import re
import time
import requests
import urllib
import os
import json
import urllib2
import ssl
import sys

reload(sys)
sys.setdefaultencoding='utf-8'
ssl._create_default_https_context = ssl._create_unverified_context
packDir = "/home/apigw/uploadPackage/"
login_url='https://172.17.192.202:8443/CMService/login.do'
logoutUrl = "https://172.17.192.202:8443/CMService/loginout.do"
url = "https://172.17.192.202:8443/CMService/uploadServicePackage.do"
accountProfileUrl = "https://172.17.192.202:8443/CMService/getuserlist.do"
checkurl = "https://172.17.192.202:8443/CMService/viewuploadedservicepackagelist.do"
data = { "userID": 'SYSADM', "userPassword": 'PASSWORD'}
environmentID = "MEM"


# manage cookie
cookieJar = http.cookiejar.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]

postData = urllib.urlencode(data)
tk = opener.open(login_url,postData)
token = tk.read()
print(token)
tokdic = json.loads(token)
loginToken=tokdic['data']['token']

with open('./cookie','w') as f:
	f.write(str(cookieJar))
cookie = ""
for item in cookieJar:
    print(item.name +"="+item.value )
    cookie += item.name +"="+item.value + ";"

def post(fileName,systemID,environmentID):
    print(fileName, systemID, environmentID)
    headers = {
    'host': "172.17.192.202:8443",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv64.0) Gecko/20100101 Firefox/64.0",
    'accept': "*/*",
    'accept-language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'accept-encoding': "gzip, deflate, br",
    'referer': "https//172.17.192.202:8443/upgradePackageDeployment.html?token=" + loginToken,
    'x-requested-with': "XMLHttpRequest",
    'content-length': "2033",
    'connection': "keep-alive",
    'cookie': cookie,
    'pragma': "no-cache",
    'cache-control': "no-cache",
    }
    files = {
        "file": (fileName, open(packDir + fileName, 'rb'), "application/x-zip-compressed"),
        'token':(None, loginToken) ,
        'systemID':(None, systemID) ,
		'superToken':(None, loginToken) ,
        'ieversion':(None, "Firefox") ,
        'environmentID':(None, environmentID) ,
        'scheduleDeploymentTime':(None, "") ,
    }
    response = requests.request("POST", url, files=files,headers=headers,verify=False)
#    print(response.request.body)
    print('PUSH ' + response.text.encode('utf-8'))

f=open(packDir+"fileList","r")
for fil in f:
	fileName = fil.split(" ")[0]
  	systemID = fil.split(' ')[1].replace("\n", "")	
	post(fileName,systemID,environmentID)
f.close

def checkDeploy(fileName,systemID,environmentID):
    headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh; q=0.8",
    'Connection': "keep-alive",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': cookie ,
    'Host': "172.17.192.202:8443",
    'Referer': "https://172.17.192.202:8443/CMService/viewuploadedservicepackagelist.do?token=" + loginToken ,
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest"
    }	
    param = {
        'environmentID': environmentID ,
        'token': loginToken ,
        'systemID': systemID ,
    }
    response = getaccountProfiles().get(checkurl,params=param,headers=headers,verify=False)
    #result=json.loads(response.text.encode('utf-8'))
    #for fname in result['data']:
    #	if fname.get('servicePackageName') == fileName:
    #		print(fname.get('servicePackageName') + fname.get('status').replace('"status":"02"','已部署')) 
    result=str(response.text.encode('utf-8')).replace("},{","},\n{").replace('"status":"02"','已部署').replace('"status":"01"','等待部署').replace('"status":"00"','已上传')
    print result
def logout():
    headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh; q=0.8",
    'Connection': "keep-alive",
    'Content-Length': "50",
    'Cookie': cookie ,
    'Host': "172.17.192.202:8443", 
    'Origin': "https://172.17.192.202:8443",
    'Referer': "https://172.17.192.202:8443/userMangement.html?token=" + loginToken ,
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest"
    }
    files = {
    	'token': loginToken ,
    	'superToken': loginToken
    }
    
    response = requests.request("POST",logoutUrl,headers=headers,data=files,verify=False)
    print(response.text.encode('utf-8'))

def getaccountProfiles():
	headers = {
	'Accept': "*/*",
	'Accept-Encoding': "gzip, deflate, br",
	'Accept-Language': "zh-CN,zh; q=0.8",
	'Connection': "keep-alive",
    'Cookie': cookie,
	'Host': "172.17.192.202:8443",
	'Referer': "https://172.17.192.202:8443/CMService/viewuploadedservicepackagelist.do?token=" + loginToken ,
	'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
	'X-Requested-With': "XMLHttpRequest"
	}			
	params = {
	'token': loginToken ,
	'superToken': loginToken ,
	'flag': "login"	
	}
	useSession = requests.Session()
	#response = requests.get(accountProfileUrl, params=params,verify=False)
	response = useSession.get(accountProfileUrl, params=params,headers=headers,verify=False)
	return useSession
f=open(packDir+"fileList","r")
#time.sleep(5)

#useSession = getaccountProfiles()

for fil in f:
    time.sleep(1)
    fileName = fil.split(" ")[0]
    systemID = fil.split(' ')[1].replace("\n", "")
    checkDeploy(fileName,systemID,environmentID)
f.close

logout()	
