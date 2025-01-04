#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.01.单个ipSSH登录交换机.py
Time    :   2025/01/04 13:10:06
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time

ip = '192.168.235.2'
username = 'test'
password = 'test'

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