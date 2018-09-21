#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "sustechoj@126.com"  # 用户名
mail_pass = "sustcoj123"  # 口令

sender = 'sustechoj@126.com'
receivers = ['11210162@mail.sustc.edu.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('CS303 Password Reset Service...', 'plain', 'utf-8')
message['From'] = sender
message['To'] = ";".join(receivers)

subject = 'CS303 Password Reset Service'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.close()
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")