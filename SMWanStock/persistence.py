# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
import time

from openpyxl import Workbook

from SMWanStock import config


class Persistence:

    """
     数据保存到excel
    """
    def __init__(self, filename):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Sheet01"
        #self.ws.append(["买卖操作", "股票代码", "股票简称", "成本", "数量"])
        self.filename = filename

    def write(self, row):
        # Rows can also be appended
        self.ws.append([row[0], row[1], row[2], row[3], row[4]])

    def save2xlsx(self):
        self.wb.save(self.filename)

    def save2xlsx4date(self,newfile):
        self.wb.save(newfile)

    def close(self):
        self.wb.close()

if __name__ == "__main__":
    #Persistence(r"E:\Git\turkeyGame\var\sample-" + stime + "-" + str(name) + ".xlsx")
    conf = config.Config('../tests/conf.ini')
    print(conf.get("FILE", "path") + conf.get("FILE", "file"))

    ps =  Persistence(conf.get("FILE", "path") + conf.get("FILE", "file"))
    rows = [12,23,45,"xx",23]
    ps.write(rows)
    ps.save2xlsx4date(r"E:\Git\turkeyGame\var\sample-xx.xlsx")
    ps.save2xlsx()

    ps.close()

