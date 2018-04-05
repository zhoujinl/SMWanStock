# -*- coding:utf-8 -*-
import sys,os,time
import ConfigParser

from SMWanStock.load import Load


class Config:
    def __init__(self, file):
        self.file = file
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.file)

    def get(self, section, key):
        try:
            return self.cf.get(section, key)
        except:
            return ""

    def set(self, section, key, value):
        try:
            self.cf.set(section, key, value)
            self.cf.write(open(self.file,'w'))
        except:
            return False
        return True

def read_config(config_file_path, field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result

def write_config(config_file_path, field, key, value):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        cf.set(field, key, value)
        cf.write(open(config_file_path,'w'))
    except:
        sys.exit(1)
    return True

if __name__ == "__main__":
    conf =  Config("../tests/conf.ini")
    print(conf.get("FILE","path"))
    #ld = Load(conf.get("FILE","path"))
    #ld.read()
    import re
    a = 'B 000935 四川爽吗 21.18 2700'
    b=re.sub(u'[^A-Za-z0-9_\s.]',r'',a)
    b = b.replace('  ', ' ')
    print(b.split(" "))


