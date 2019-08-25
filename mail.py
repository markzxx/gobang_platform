#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "sustechai@126.com"  # 用户名
mail_pass = "123456abc"  # 口令

async def send_verify_code(sid, verify_code):
    receiver = "{}@mail.sustech.edu.cn".format(sid)
    message = MIMEText('Dear {}:\n\nYour verify code is {}.\n\nCS303'.format(sid, verify_code), 'plain', 'utf-8')
    message['From'] = mail_user
    message['To'] = receiver

    subject = 'CS303 Password Reset Service'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receiver, message.as_string())
        smtpObj.close()
    except smtplib.SMTPException as e:
        print(e)

if __name__ == '__main__':
    #測試
    send_verify_code(11210162, 123)