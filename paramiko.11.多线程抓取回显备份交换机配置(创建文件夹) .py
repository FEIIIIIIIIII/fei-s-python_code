#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.11.多线程抓取回显备份交换机配置(创建文件夹) .py
Time    :   2025/01/04 13:08:46
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import datetime
import os
import threading
from queue import Queue

#导入getpass模块，用于隐藏输入密码
import getpass

#导入re模块，用于正则表达式匹配字符
import re

username = input('Username: ')
password = getpass.getpass('Password: ')

print(f'程序开始执行时间 {time.strftime('%X')}')

threads = []

# 获取当前日期
current_date = datetime.datetime.now()
current_datetime = current_date.strftime(f'%Y-%m-%d')

#创建文件夹，用于保存设备的备份配置
os.mkdir('./backup_%s' %(current_datetime))

#打开ip文件，赋值给iplist
iplist = open('ip_list.txt') 

def ssh_session(ip,output_q):
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

    back_config = open('./backup_%s/'%(current_datetime) + ip + '_backupconfig.txt','a')

    output = re.sub(r'---- More ----.*42D','',output)
    back_config.write(output)
    back_config.close()
    print('已经成功备份交换机配置' + ip)

    command.send('quit\n')
    ssh_client.close()

for x in iplist.readlines():
    t = threading.Thread(target=ssh_session,args=(x.strip(),Queue()))
    t.start()
    threads.append(t)

for i in threads:
    i.join()

iplist.close()
print(f'程序结束执行时间 {time.strftime('%X')}')