
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib

page = 1
url = "http://www.newsmth.net/nForum/#!article/SMIF/1074107?p=20"
loginUrl = "http://www.newsmth.net/nForum/user/ajax_login.json"
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            "Referer":"http://www.newsmth.net/nForum/",
            "Host":"www.newsmth.net",
            "Origin":"http://www.newsmth.net",
            "X-Requested-With":"XMLHttpRequest"}

cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
postdata = urllib.urlencode({
            'id':'jalon',
            'passwd':'513513'
        })
request =  urllib2.Request(loginUrl,postdata,headers)
response = opener.open(request)
loginMsg = response.read().decode("GBK")
print(loginMsg)

pageUrl = "http://www.newsmth.net/nForum/article/SMIF/1074107?ajax&p=22&_t=1522769157210"
response = opener.open(pageUrl)
pageMsg= response.read().decode("GBK")
print(pageMsg)



# pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?' +
#                      'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
# items = re.findall(pattern, content)
# for item in items:
#     haveImg = re.search("img", item[3])
#     if not haveImg:
#         print item[0], item[1], item[2], item[4]
