# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

'''
网易126邮箱，使用 用户名+授权码 进行登陆
设置->客户端授权密码 z*1*
'''

class Notify:

    def __init__(self,host,user,passwd,sender,receivers,port=25):
        # 第三方 SMTP 服务
        self.host = host  # SMTP服务器
        self.port = port  # SMTP端口
        self.user = user  # 用户名
        self.passwd = passwd  # 口令

        self.sender = sender  #发件人邮箱
        self.receivers = receivers  # 接收人邮箱列表，支持多人发送
        self.subject = '水木社区通知'

    def send(self,msg):
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header('Jalon')
        message['To'] = Header('JalonStock')
        message['Subject'] = Header(self.subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.host, self.port)  # 25 为 SMTP 端口号
            smtpObj.login(self.user, self.passwd)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException,e :
            print "Error: 无法发送邮件",e.args

if __name__ == "__main__":
    #notf = Notify("smtp.126.com","zhoujinl","*****","zhoujinl@126.com","zhoujinl@126.com")
    notf = Notify("mail.ffcs.cn","zhoujl","****","zhoujl@ffcs.cn","zhoujinl@126.com")
    notf.send("Cesi 中华狮山")
