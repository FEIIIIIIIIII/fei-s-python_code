#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.06.try和except处理异常问题.py
Time    :   2025/01/04 13:09:23
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import getpass
import sys
import socket

username = input('Username: ')
password = getpass.getpass('Password: ')   #getpass用来隐藏输入密码
ip_file = sys.argv[1]     #运行命令python3 06.try和except处理异常问题.py ip1.txt cmd1.txt时，ip1.txt文本内容赋值给ip_file
cmd_file = sys.argv[2]    #运行命令python3 06.try和except处理异常问题.py ip1.txt cmd1.txt时，cmd1.txt文本内容赋值给cmd_file
#如有其他版本的交换机，可以用ip2、ip3、ip4、、、cmd2、cmd3、cmd4、、、进行运行python3命令

switch_with_authentication_issue = []    #建立一个认证登录交换机有问题的列表
switch_not_reachable = []    #建立一个网络不可达交换机的列表

iplist = open(ip_file, 'r')    #只读模式读取ip_file内存数据，赋值给iplist
for x in iplist.readlines():    #逐行读取，赋值给x
    try:
        ip = x.strip()          #strip()去掉读取当前行的换行符
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
        print('已经成功登录交换机', ip)
        command = ssh_client.invoke_shell()     #获取配置命令窗口给command
        cmdlist = open(cmd_file, 'r')
        cmdlist.seek(0)              #每次读取配置文件，读取光标都移到最前，从头开始读取
        for x in cmdlist.readlines():
            command.send('screen-length 0 temporary\n')    #关闭分屏功能
            command.send(x + '\n')
            time.sleep(1)            #执行完上一条命令，等待1秒再继续执行下一条命令
        cmdlist.close()
        output = command.recv(65535).decode('ascii')  #以ASCII编码方式进行输出给output
        print(output)      #显示器打印出2个for循环的配置情况
    except paramiko.ssh_exception.AuthenticationException:  #如果没有try和except，运行python脚本，用户验证失败，python会报错：paramiko.ssh_exception.AuthenticationException：Authentication Failed。此行命令是进行匹配报错信息进行处理异常。
        print(ip + '用户验证失败！')
        switch_with_authentication_issue.append(ip)
    except socket.error:
        print(ip + '目标不可达！')
        switch_not_reachable.append(ip)

iplist.close()
ssh_client.close()

print('\n下列交换机用户验证失败，请检查：')
for x in switch_with_authentication_issue:
    print(x)

print('\n下列交换机ip不可达，请检查：')
for x in switch_not_reachable:
    print(x)