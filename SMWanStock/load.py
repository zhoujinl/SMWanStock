# -*- coding:utf-8 -*-

from openpyxl import load_workbook
from openpyxl import Workbook

class Load:

    """ 从excel读取数据"""

    def __init__(self, filename):
        self.wb = load_workbook(filename)
        self.ws =  self.wb['SMWanstock']


    def read(self):
        for row in self.ws.iter_rows(min_row=2, ):  # 去掉标题
            #print(row[1].value)
            for cell in row:
                print(cell.value)

    def close(self):
        self.wb.close()

if __name__ == "__main__":
    ld = Load(r"../tests/test.xlsx")
    ld.read()

