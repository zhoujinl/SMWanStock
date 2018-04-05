# -*- coding:utf-8 -*-

import tushare
import lxml.html
import pandas
import numpy
import bs4

print(tushare.__version__)
import tushare as ts

#获取股票分类信息
#print(ts.get_concept_classified())

#print(ts.get_stock_basics())
# 获取个股分时信息
print(ts.get_realtime_quotes('000581'))

#获取大盘实时行情
print( ts.get_index())