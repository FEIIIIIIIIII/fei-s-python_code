#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.03.getpass和for循环登录交换机.py
Time    :   2025/01/04 13:09:44
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import getpass

username = input('Username: ')

#隐藏输入密码
password = getpass.getpass('Password: ') 

#登录11,12,13,14,15 ip尾数交换机
for i in range(11,16): 
    ip = '192.168.2.' + str(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
    command = ssh_client.invoke_shell()
    
    print('已经成功登录交换机'+ip)
    
    command.send('display current-configuration\n')
    time.sleep(3)
    command.send(' ')
    
    output = command.recv(65535).decode('ascii')
    print(output)

ssh_client.close()