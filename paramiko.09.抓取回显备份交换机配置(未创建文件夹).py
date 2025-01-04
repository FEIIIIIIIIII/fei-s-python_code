#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.09.抓取回显备份交换机配置(未创建文件夹).py
Time    :   2025/01/04 13:09:04
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import datetime
import os

#导入getpass模块，用于隐藏输入密码
import getpass

#导入re模块，用于正则表达式匹配字符
import re

username = input('Username: ')
password = getpass.getpass('Password: ')

#打开ip文件，赋值给iplist
iplist = open('ip_list.txt') 

#逐行读取，赋值给x
for x in iplist.readlines():
    #strip()去掉换行符
    ip = x.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
    command = ssh_client.invoke_shell()

    print('已经成功登录交换机' + ip)
    
    command.send('screen-length 10 temporary\n')
    command.send('display current-configuration\n')
    time.sleep(0.5)
    
    output = ''
        
    while True:
        outputing = command.recv(65535).decode('ascii')
        output = output + outputing
        if outputing.endswith('>'):
            break
        if '---- More ----' in outputing:
           command.send(' ')
           time.sleep(0.5)
    
    # 获取当前日期
    current_date = datetime.datetime.now()
    current_datetime = current_date.strftime(f'%Y-%m-%d')

    back_config = open(ip + '_backconfig_%s.txt' %(current_datetime),'a')

    output = re.sub(r'---- More ----.*42D','',output)
    back_config.write(output)
    back_config.close()
    print('已经成功备份交换机配置' + ip)

    command.send('quit\n')

iplist.close()
ssh_client.close()