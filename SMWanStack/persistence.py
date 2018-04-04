# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
import time

'''
需要模拟帐号登陆的过程，再从中抓取用户登陆的Url,网页输出内容的url
'''
class SmSpider:
    def __init__(self):
        self.cookies =  cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies ))
        self.postdata = urllib.urlencode({
            'id': 'jalon',
            'passwd': '513513'
        })
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            "Referer": "http://www.newsmth.net/nForum/",
            "Host": "www.newsmth.net",
            "Origin": "http://www.newsmth.net",
            "X-Requested-With": "XMLHttpRequest"}
        self.loginUrl = "http://www.newsmth.net/nForum/user/ajax_login.json"
        self.pageUrlPre = "http://www.newsmth.net/nForum/article/SMIF/1074107?ajax&p="
        self.pageCount = 1
        self.stockList = []

    def __login__(self):
        request = urllib2.Request(self.loginUrl, self.postdata, self.headers)
        self.opener.open(request)

    def __getPageCount__(self):
        pageUrl = self.pageUrlPre + "1"
        request = urllib2.Request(pageUrl,headers=self.headers)
        response = self.opener.open(request)
        pageMsg = response.read().decode('GBK')
        # print(pageMsg)
        # 帖子个数和文章数是一致的
        pattern = re.compile('<ul class="pagination"><li class="page-pre">.*?<i>(.*?)</i>', re.S)
        postCount = re.findall(pattern, pageMsg)
        self.pageCount = int(postCount[0]) / 10 + 1

    def __getPageStocks__(self,pageIndex):
        request =  urllib2.Request(self.pageUrlPre+str(pageIndex),headers=self.headers)
        response = self.opener.open(request)
        pageMsg= response.read().decode("GBK")
        #print(pageMsg)

        ## 解析页面
        pattern = re.compile('<td class="a-content">.*?<br />&nbsp;&nbsp;<br />(.*?)--.*?</td>', re.S)
        items = re.findall(pattern, pageMsg)
        for item in items:
            post = item.encode("UTF-8")
            if post.find("在 wanxiaotong 的大作中提到:") < 0 :  # 排除回复部分的内容
                if  post.find("S") >-1  or post.find("B") > -1:
                    rows = post.replace("&nbsp;","").strip()
                    rowList = map(lambda s: s and s.strip(), rows.split("<br />"))
                    self.stockList.extend( rowList)

        ## 过滤无用数据
        self.stockList = filter(lambda s : s and s.strip() ,self.stockList)
        self.stockList = filter(lambda s : s.startswith("S")  or s.startswith("B")  ,self.stockList)


    def getStocks(self):
        self.__login__()
        self.__getPageCount__()
        # self.__getPageStocks__(2)
        # int(self.pageCount) + 1
        for index in  range(1,int(self.pageCount) + 1) :
            time.sleep(1)
            self.__getPageStocks__(index)

# ## 构造请求头部和cookies 设置登陆帐号密码
# cookies = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
# postdata = urllib.urlencode({
#             'id':'jalon',
#             'passwd':'513513'
#         })
# headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
#             "Referer":"http://www.newsmth.net/nForum/",
#             "Host":"www.newsmth.net",
#             "Origin":"http://www.newsmth.net",
#             "X-Requested-With":"XMLHttpRequest"}
#
# ## 登陆页面
# loginUrl = "http://www.newsmth.net/nForum/user/ajax_login.json"
# request =  urllib2.Request(loginUrl,postdata,headers)
# response = opener.open(request)
# loginMsg = response.read().decode("GBK")
# #print(loginMsg)
#
# ## 网页内容
# pageUrlPre="http://www.newsmth.net/nForum/article/SMIF/1074107?ajax&p="
# pageUrlSuf=16
# pageUrl = pageUrlPre + str(pageUrlSuf)
# response = opener.open(pageUrl)
# pageMsg= response.read().decode("GBK")
# #print(pageMsg)
#
# ## 解析页面
#
# pattern = re.compile('<td class="a-content">.*?<br />&nbsp;&nbsp;<br />(.*?)--.*?</td>', re.S)
# items = re.findall(pattern, pageMsg)
# stockkList = []
# for item in items:
#     sitem = item.encode("UTF-8")
#     #print (sitem)
#     if sitem.find("在 wanxiaotong 的大作中提到:") < 0 :
#         if  sitem.find("S") > -1 or sitem.find("B") > -1:
#             #print (sitem.replace("<br />","").replace("&nbsp;",""))
#             rows = sitem.replace("&nbsp;","").strip()
#             #print(rows)
#             stockkList.extend( rows.split("<br />"))
#
#
# stockkList = filter(lambda s : s and s.strip() ,stockkList)
#
# for item in stockkList :
#     print(item.strip())


smSpider = SmSpider()
smSpider.getStocks()
print (len(smSpider.stockList))
for item in smSpider.stockList :
    print(item.strip())

