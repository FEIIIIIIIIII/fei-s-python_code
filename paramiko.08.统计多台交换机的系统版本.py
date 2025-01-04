#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.08.统计多台交换机的系统版本.py
Time    :   2025/01/04 13:09:10
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import datetime

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
    
    command.send('display version\n')
    time.sleep(1)
    
    output = command.recv(65535).decode('ascii')

    #re.findall()函数返回值是字典，需要转换为字符串str，用于打印输出
    #正则表达式r'Version.*\)'，意思是匹配 'Version***多个任意字符***00)',Version开头，00)结束，)需要\进行转义
    device_version = str(re.findall(r'Version.*\)',output))

    print('设备ip: %s的系统版本是 '%(ip) + device_version)
    
    # 获取当前日期
    current_date = datetime.datetime.now()
    current_datetime = current_date.strftime(f'%Y-%m-%d')

    devices_version = open('devices_version-%s.txt'%(current_datetime),'a')
    devices_version.write('设备ip: %s的系统版本是 '%(ip) + device_version + '\n')
    devices_version.close()

    command.send('quit\n')

iplist.close()
ssh_client.close()