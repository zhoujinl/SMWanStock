# -*- coding:utf-8 -*-
import socket
import urllib2

import requests
from bs4 import BeautifulSoup
import csv

from SMWanStock.load import Load
from SMWanStock.persistence import Persistence

'''
fork from https://github.com/Jennifer1996/Projects
'''
def IPspider(numpage):
    ps =  Persistence(r'E:\Git\SMWanStock\tests\data\ips.xlsx')
    url = 'http://www.xicidaili.com/nn/'
    user_agent = 'IP'
    headers = {'User-agent': user_agent}
    for num in xrange(1, numpage + 1):
        ipurl = url + str(num)
        print 'Now downloading the ' + str(num * 100) + ' ips'
        request = urllib2.Request(ipurl, headers=headers)
        content = urllib2.urlopen(request).read()
        #print(content)
        bs = BeautifulSoup(content,"lxml")
        res = bs.findAll('tr')
        for item in res:
            try:
                temp = []
                tds = item.find_all('td')
                temp.append(tds[1].text.encode('utf-8'))
                temp.append(tds[2].text.encode('utf-8'))
                ps.write(temp)
                #print(temp)
            except IndexError:
                pass
    ps.save2xlsx()
    ps.close()

# 假设爬取前十页所有的IP和端口
IPspider(2)

def IPpool():
    ld = Load(r'E:\Git\SMWanStock\tests\data\ips.xlsx')
    ld.read()
    IPpool=[]
    for row in ld.rowList:
        row =  row.split(",")
        proxies = {
            "http": "http://122.114.31.177:808",
            "https": "http://177.21.127.58:20183",
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            "X-Requested-With": "XMLHttpRequest"}


        html = requests.get('http://www.ip138.com/', headers=headers, proxies=proxies).text  # .decode('utf-8')
        print html.encode('utf-8')


    return IPpool

print(IPpool())