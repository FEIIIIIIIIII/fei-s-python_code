#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.04.登录IP不连续的交换机.py
Time    :   2025/01/04 13:09:38
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import getpass

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
    
    command.send('screen-length 0 temporary\n')
    time.sleep(1)
    command.send('display current-configuration\n')
    time.sleep(3)
    command.send('screen-length 24 temporary\n')
    time.sleep(1)

    output = command.recv(65535).decode('ascii')
    print(output)

iplist.close()
ssh_client.close()