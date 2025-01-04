#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.07.备份多台华为交换机配置,ftp的put方式.py
Time    :   2025/01/04 13:09:17
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import getpass

username = input('Username：')
password = getpass('Password：')

f = open('ip_list.txt')

for line in f.readlines():
    ip_address = line.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=ip_address,username=username,password=password,look_for_keys=False)
    print('已经成功登录交换机', ip_address)

    command = ssh_client.invoke_shell()

    #登录ftp服务器，假设ftp服务器ip地址是192.168.1.254
    command.send('ftp 192.168.1.254\n')
    time.sleep(1)

    #输入ftp用户名和密码，假设用户名是ftpuser，密码是ftppassword
    command.send('ftpuser\n')
    time.sleep(1)
    command.send('ftppassword\n')

    #设置二进制传输方式
    command.send('binary\n')

    #上传交换机配置文件到ftp服务器
    command.send('put vrpcfg.zip ' + ip_address + '_vrpcfg.zip' + '\n')
    time.sleep(3)

    #网络设备退出登录ftp服务器
    command.send('quit\n')

    #如果ftp部署在windows上，因为中文编码原因，解码不能用ACSII，要用GB2312
    output = command.recv(65535)
    print(output.decode('GB2312'))

f.close()
ssh_client.close()