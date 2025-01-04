#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   paramiko.12.多线程控制线程数抓取回显备份交换机配置(创建文件夹) .py
Time    :   2025/01/04 13:07:14
Author  :   afei 
Version :   python 3.11
'''

import paramiko
import time
import datetime
import os
from concurrent.futures import ThreadPoolExecutor

#导入getpass模块，用于隐藏输入密码
import getpass

#导入re模块，用于正则表达式匹配字符
import re

username = input('Username: ')
password = getpass.getpass('Password: ')

start_time = datetime.datetime.now()

threads = []

# 获取当前日期
current_date = datetime.datetime.now()
current_datetime = current_date.strftime(f'%Y-%m-%d')

#创建文件夹，用于保存设备的备份配置
os.mkdir('./backup_%s' %(current_datetime))

def ssh_session(ip):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
    command = ssh_client.invoke_shell()

    print('已经成功登录交换机' + ip + ',开始备份配置')
    
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

#打开ip文件，赋值给iplist
iplist = open('ip_list.txt')
ips = []

#转换成列表list，ips = ['ip1','ip2'.......'ipx']
for i in iplist.readlines():
    ips.append(i.strip())

iplist.close()

#根据服务器性能设置线程数max_workers=?，即同一时间备份多少台设备配置
with ThreadPoolExecutor(max_workers=10) as exe:
    #ssh_session为传递进去的单个执行函数名，ips为ip列表
    exe.map(ssh_session,ips)

print('备份任务开始时间：' + start_time.strftime("%Y年%m月%d日%H时%M分%S秒"))
end_time = datetime.datetime.now()
print('备份任务结束时间：' + end_time.strftime("%Y年%m月%d日%H时%M分%S秒"))
run_time = end_time-start_time
hours, remainder = divmod(run_time.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
print(f"本次备份任务运行时间：{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒")