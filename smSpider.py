# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
import time

from SMWanStock.load import Load
from SMWanStock.notify import Notify
from SMWanStock.persistence import Persistence
from SMWanStock.stock import Stock

'''
需要模拟帐号登陆的过程，再从中抓取用户登陆的Url,网页输出内容的url
'''
class SmSpider:
    def __init__(self):
        self.cookies =  cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies ))
        self.opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'http://127.0.0.1:1080'}))

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
        pageMsg= response.read().decode("GBK")  #网页编码GBK，因此需解码后再用UTF-8加密，因此python环境是utf
        pageMsg = pageMsg.encode("UTF-8")
        #print(pageMsg)

        ## 解析页面
        pattern = re.compile('<td class="a-content">.*?发信站.*?水木社区 (.*?)站内.*?&nbsp;&nbsp;<br />(.*?)--.*?</td>', re.S)
        items = re.findall(pattern, pageMsg)
        #print (items)
        ## [('(Tue Jan&nbsp;&nbsp;2 15:23:39 2018), ', ' B 600691 107000 3.95 <br /> B 000807 13900 10.62 <br /> B 000878 7700 14.30 <br /> B 600516 3400 29.83 <br /> B 300726 2300 29.44 <br /> B 603937 2500 26.72 <br /> B 603076 1000 39.70 <br />&nbsp;&nbsp;<br /> '), ('(Tue Jan&nbsp;&nbsp;2 15:24:18 2018), ', ' \xe7\x9b\xb4\xe6\x8e\xa5\xe6\x8c\x89\xe7\x85\xa7\xe6\x94\xb6\xe7\x9b\x98\xe4\xbb\xb7\xe6\xa0\xbc\xe5\xa1\xab\xe5\x86\x99\xef\xbc\x8c\xe5\xbc\x80\xe5\xa7\x8b\xe7\x9a\x84\xe6\x97\xb6\xe5\x80\x99\xe6\xb2\xa1\xe6\x9c\x89\xe5\x86\x99\xe6\x8c\x81\xe4\xbb\x93\xef\xbc\x8c\xe5\x9c\xa8\xe8\xbf\x99\xe9\x87\x8c\xe4\xb8\x80\xe5\xb9\xb6\xe6\x8a\x84\xe4\xb8\x8b\xe6\x9d\xa5 <br /> '), ('(Wed Jan&nbsp;&nbsp;3 15:20:45 2018), ', ' B 300009 1100 26.12 <br /> B 600383 2400 13.81 <br /> B 600383 3200 13.82 <br /> B 600516 2000 30.56 <br /> S 300726 2200 28.88 <br /> S 300726 100 28.67 <br /> S 603937 2500 24.90 <br /> S 603076 1000 37.75 <br /> '), ('(Thu Jan&nbsp;&nbsp;4 10:21:54 2018), ', ' S 600691 3.94 10000 <br /> B 600801 15.54 2200 <br /> B 600801 15.58 3300 <br /> '), ('(Thu Jan&nbsp;&nbsp;4 10:26:06 2018), ', ' B 600985 15.09 1700 <br /> '), ('(Thu Jan&nbsp;&nbsp;4 12:43:10 2018), ', ' \xe8\xbf\x99\xe6\xb0\xb4\xe6\xb3\xa5\xe8\xa6\x81\xe6\x98\xaf\xe5\x8a\xa0\xe5\x9c\xa8\xe6\x96\xb9\xe5\xa4\xa7\xe4\xb8\x8a\xe8\xaf\xa5\xe5\xa4\x9a\xe5\xa5\xbd\xef\xbc\x8c\xe5\x93\x8e <br /> \xe3\x80\x90 \xe5\x9c\xa8 wanxiaotong \xe7\x9a\x84\xe5\xa4\xa7\xe4\xbd\x9c\xe4\xb8\xad\xe6\x8f\x90\xe5\x88\xb0: \xe3\x80\x91 <br /> <font class="f006">: S 600691 3.94 10000 </font> <br /> <font class="f006">: B 600801 15.54 2200 </font> <br /> <font class="f006">: B 600801 15.58 3300 </font> <br />&nbsp;&nbsp;<br /> '), ('(Thu Jan&nbsp;&nbsp;4 12:43:44 2018), ', ' \xe6\x96\xb9\xe5\xa4\xa7\xe5\x8a\xa0\xe5\xb0\x91\xe4\xba\x86\xef\xbc\x9f <br /> \xe3\x80\x90 \xe5\x9c\xa8 wanxiaotong \xe7\x9a\x84\xe5\xa4\xa7\xe4\xbd\x9c\xe4\xb8\xad\xe6\x8f\x90\xe5\x88\xb0: \xe3\x80\x91 <br /> <font class="f006">: B 300009 1100 26.12 </font> <br /> <font class="f006">: B 600383 2400 13.81 </font> <br /> <font class="f006">: B 600383 3200 13.82 </font> <br /> <font class="f006">: ................... </font> <br />&nbsp;&nbsp;<br /> '), ('(Thu Jan&nbsp;&nbsp;4 13:04:40 2018), ', ' B 600426 17.42 1500 <br /> '), ('(Thu Jan&nbsp;&nbsp;4 13:32:57 2018), ', ' \xe6\x98\x8e\xe6\x98\x8e\xe7\x9f\xa5\xe9\x81\x93\xe4\xb8\x87\xe5\xb9\xb4\xe9\x9d\x92\xe6\x98\xaf\xe9\xbe\x99\xe5\xa4\xb4\xef\xbc\x8c\xe5\x8d\xb4\xe6\x83\xb3\xe7\x9d\x80\xe6\xb0\xb4\xe6\xb3\xa5\xe5\x90\x8c\xe8\xb4\xa8\xe5\x8c\x96\xef\xbc\x8c\xe5\x8e\xbb\xe4\xb9\xb0\xe4\xb8\xaa\xe5\x8d\x8e\xe6\x96\xb0\xe6\x8c\x87\xe6\x9c\x9b\xe7\xaf\xa1\xe4\xbd\x8d\xef\xbc\x8c\xe5\x93\x8e <br /> \xe3\x80\x90 \xe5\x9c\xa8 wanxiaotong \xe7\x9a\x84\xe5\xa4\xa7\xe4\xbd\x9c\xe4\xb8\xad\xe6\x8f\x90\xe5\x88\xb0: \xe3\x80\x91 <br /> <font class="f006">: S 600691 3.94 10000 </font> <br /> <font class="f006">: B 600801 15.54 2200 </font> <br /> <font class="f006">: B 600801 15.58 3300 </font> <br />&nbsp;&nbsp;<br /> '), ('(Thu Jan&nbsp;&nbsp;4 13:40:44 2018), ', ' S 600383 13.85 1000 <br /> ')]
        ## TODO  这里是否需要对每个交易生成对象封装
        for per in items:
            tradeTime = per[0].replace("&nbsp;"," ").replace("(","").replace("),","")
            post = per[1]
            if post.find("在 wanxiaotong 的大作中提到:") < 0 :  # 排除回复部分的内容
                if  post.find("S") >-1  or post.find("B") > -1:
                    rows = post.replace("&nbsp;","").strip()
                    rowList = map(lambda s: s and s.strip(), rows.split("<br />"))

                    rowList = filter(lambda s: s.startswith("S") or s.startswith("B"), rowList)
                    rowList = map(lambda s: re.sub(u'[^A-Za-z0-9_\s.]', r'', s), rowList)  ## 清除股票中文简称
                    rowList = map(lambda s: s.replace('  ', ' '), rowList)
                    rowList = map(lambda s: s.replace(' ', ','), rowList)
                    rowList = map(lambda s: s + "," + tradeTime, rowList)  #增加时间字段  B,600691,107000,3.95,Tue Jan  2 15:23:39 2018
                    rowList = map(lambda s: s.rstrip(), rowList)

                    #print (rowList)
                    self.stockList.extend( rowList)

    def shuffleStockList(self):
        ## 过滤无用数据
        #self.stockList = filter(lambda s: s and s.strip(), self.stockList)
        #self.stockList = filter(lambda s: s.startswith("S") or s.startswith("B"), self.stockList)

        # S 603683 26.38 2500
        # B 000935 四川双马 21.18 2700
        ## 清除股票中文简称
        #self.stockList = map(lambda s: re.sub(u'[^A-Za-z0-9_\s.]',r'',s), self.stockList)
        #self.stockList = map(lambda s: s.replace('  ', ' '), self.stockList)
        pass

    def getStocks(self):
        self.__login__()
        self.__getPageCount__()
        # self.__getPageStocks__(2)
        # int(self.pageCount) + 1
        for index in  range(1,int(self.pageCount) + 1) :
            self.__getPageStocks__(index)
        self.shuffleStockList()

    def persistence(self,perst):
        perst.write(["买卖操作", "股票代码", "成本", "数量","交易时间"])
        for stock in self.stockList:
            perst.write(stock.split(","))
        perst.save2xlsx()
        pass

if __name__ == '__main__':

    from optparse import OptionParser
    from SMWanStock import config

    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="conf", help="The conf file to load", default='./tests/conf.ini', type="str")

    (options, args) = parser.parse_args()
    # 获取配置文件
    conf = config.Config(options.conf)
    fileName = conf.get("FILE","path") + conf.get("FILE","file")
    isNotify = conf.get("BASE","notify")

    # 获取sm交易信息
    smSpider = SmSpider()
    smSpider.getStocks()
    smSpider.stockList


    # 创建加载对象,获得stock列表
    latestLoad = Load(fileName)
    latestLoad.read()
    latestLoad.rowList

    diffList = []
    ## 对比是否有更新
    for i in range(len(latestLoad.rowList),len(smSpider.stockList)):
        diffList.append(smSpider.stockList[i])

    print(diffList)
    if len(diffList) > 0 :

        # 创建持久化对象，持久化操作
        latestPersistence = Persistence(fileName)
        # smSpider.persistence(latestPersistence)
        latestPersistence.close()

        if bool(isNotify) : # 发邮件
            st = Stock(diffList)
            st.getStockInfo()

            notf = Notify("smtp.126.com", "zhoujinl", "zy123456", "zhoujinl@126.com", "zhoujinl@126.com")
            notf.send('\r\n'.join(st.stcokInfoList))

    ##TODO 显示股票详细信息

