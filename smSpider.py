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
        self.perst = None
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
        for per in items:
            post = per.encode("UTF-8")
            if post.find("在 wanxiaotong 的大作中提到:") < 0 :  # 排除回复部分的内容
                if  post.find("S") >-1  or post.find("B") > -1:
                    rows = post.replace("&nbsp;","").strip()
                    rowList = map(lambda s: s and s.strip(), rows.split("<br />"))
                    self.stockList.extend( rowList)

    def shuffleStockList(self):
        ## 过滤无用数据
        self.stockList = filter(lambda s: s and s.strip(), self.stockList)
        self.stockList = filter(lambda s: s.startswith("S") or s.startswith("B"), self.stockList)

        # S 603683 26.38 2500
        # B 000935 四川双马 21.18 2700
        ## 清除股票中文简称
        self.stockList = map(lambda s: re.sub(u'[^A-Za-z0-9_\s.]',r'',s), self.stockList)
        self.stockList = map(lambda s: s.replace('  ', ' '), self.stockList)

    def getStocks(self):
        self.__login__()
        self.__getPageCount__()
        # self.__getPageStocks__(2)
        # int(self.pageCount) + 1
        for index in  range(1,int(self.pageCount) + 1) :
            self.__getPageStocks__(index)

        self.shuffleStockList()

    def setPersistence(self,perst):
        self.perst = perst

    def save(self):
        pass


if __name__ == '__main__':
    from optparse import OptionParser
    from SMWanStock import config

    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="conf", help="The conf file to load", default='./tests/conf.ini', type="str")

    (options, args) = parser.parse_args()
    print(options.conf)
    conf = config.Config(options.conf)
    #print (conf.get("NOTIFY","email"))
    smSpider = SmSpider()
    smSpider.getStocks()
    print (len(smSpider.stockList))
    for item in smSpider.stockList :
        print(item)

