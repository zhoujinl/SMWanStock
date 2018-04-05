# -*- coding:utf-8 -*-

import tushare
import lxml.html
import pandas
import numpy
import bs4

import tushare as ts

class Stock:
    '''
    Tushare是一个免费、开源的python财经数据接口包。
    http://tushare.org/index.html
    '''
    def __init__(self,stockList):
        self.stockList = stockList
        self.stcokInfoList = []

    def getStockInfo(self):
        for row in self.stockList:
            #print ("------------"+row)
            sr = row.split(",")

            df = ts.get_realtime_quotes(sr[1])
            code = df.ix[0,['code']].to_string().encode('utf-8').replace("    ",":")
            name = df.ix[0,['name']].to_string().encode('utf-8').replace("    ",":")
            price = df.ix[0,['price']].to_string().decode().encode('utf-8').replace("    ",":")
            high = df.ix[0,['high']].to_string().decode().encode('utf-8').replace("    ",":")
            low = df.ix[0,['low']].to_string().decode().encode('utf-8').replace("    ",":")
            time = df.ix[0, ['time']].to_string().decode().encode('utf-8').replace("    ", ":")

            info = row + " ===> " + code + ","+ name +","+ price +  "," + high + ","+ low + ","+ time
            self.stcokInfoList.append(info)


if __name__ == '__main__':
    lt = ['B,600691,107000,3.95,Tue Jan  2 15:23:39 2018', 'B,000807,13900,10.62,Tue Jan  2 15:23:39 2018']
    st = Stock(lt)
    st.getStockInfo()
    print(st.stcokInfoList)