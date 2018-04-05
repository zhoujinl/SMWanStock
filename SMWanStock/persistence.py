# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
import time

from openpyxl import Workbook

class Persistence:

    """
     数据保存到excel
    """
    def __init__(self, filename):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "SMWanstock"
        self.ws.append(["买卖操作", "股票代码", "股票简称", "成本", "数量"])
        self.filename = filename

    def write(self, row):
        # Rows can also be appended
        self.ws.append([row[0], row[1], row[2], row[3], row[4]])

    def save2xlsx(self):
        self.wb.save(self.filename)

    def close(self):
        self.wb.close()

if __name__ == "__main__":
    #Persistence(r"E:\Git\turkeyGame\var\sample-" + stime + "-" + str(name) + ".xlsx")
    ps = Persistence(r"../tests/test.xlsx")
    rows = [12,23,45,"xx",23]
    ps.write(rows)
    ps.save2xlsx()
    ps.close()

