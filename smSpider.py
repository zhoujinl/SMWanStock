# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

page = 1
url = "http://www.newsmth.net/nForum/#!article/SMIF/1074107?p=20"
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36' }

print(url)

request = urllib2.Request(url,headers = headers)
response = urllib2.urlopen(request)

content = response.read().decode("GBK")

print(content)

# pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?' +
#                      'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
# items = re.findall(pattern, content)
# for item in items:
#     haveImg = re.search("img", item[3])
#     if not haveImg:
#         print item[0], item[1], item[2], item[4]
