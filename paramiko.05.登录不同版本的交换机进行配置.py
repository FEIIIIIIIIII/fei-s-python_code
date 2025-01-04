#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.05.登录不同版本的交换机进行配置.py
Time    :   2025/01/04 13:09:33
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import getpass
import sys

username = input('Username: ')
password = getpass.getpass('Password: ')   #getpass用来隐藏输入密码
ip_file = sys.argv[1]     #运行命令python3 05.登录不同版本的交换机进行配置.py ip1.txt cmd1.txt时，ip1.txt文本内容赋值给ip_file
cmd_file = sys.argv[2]    #运行命令python3 05.登录不同版本的交换机进行配置.py ip1.txt cmd1.txt时，cmd1.txt文本内容赋值给cmd_file
                          #如有其他版本的交换机，可以用ip2、ip3、ip4、、、cmd2、cmd3、cmd4、、、进行运行python3命令

iplist = open(ip_file, 'r')    #只读模式读取ip_file内存数据，赋值给iplist

for x in iplist.readlines():    #逐行读取，赋值给x
    ip = x.strip()          #strip()去掉读取当前行的换行符
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
    print('已经成功登录交换机', ip)
    command = ssh_client.invoke_shell()     #获取配置命令窗口给command
    
    cmdlist = open(cmd_file, 'r')
    cmdlist.seek(0)              #每次读取配置文件，读取光标都移到最前，从头开始读取

    for x in cmdlist.readlines():
        command.send(x + '\n')
        time.sleep(1)            #执行完上一条命令，等待1秒再继续执行下一条命令
    cmdlist.close()
    output = command.recv(65535).decode('ascii')  #以ASCII编码方式进行输出给output
    print(output)      #显示器打印出2个for循环的配置情况

iplist.close()
ssh_client.close()