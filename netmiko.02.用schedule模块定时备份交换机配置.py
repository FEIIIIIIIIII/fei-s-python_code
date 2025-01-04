#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   netmiko.02.用schedule模块定时备份交换机配置.py
Time    :   2025/01/04 13:11:27
Author  :   afei 
Version :   python 3.11
'''

import netmiko
from netmiko import ConnectHandler
import schedule
import datetime

def back_config():
    try:
        while True:
            f = open('ip_list.txt')
            for x in f.readlines():
                ip = x.strip()
                device = {'device_type':'huawei',
                          'host':ip,
                          'username':'test',
                          'password':'test'}
                ssh__client = ConnectHandler(**device)
                output = ssh__client.send_command('display current-configuration')
        
                # 获取当前日期
                current_date = datetime.datetime.now()
                current_datetime = current_date.strftime(f'%Y-%m-%d')
                back = open(current_datetime + '-' + ip + '-bak.txt','a')
                back.write(output)
                back.close()
                print(ip + ' 配置已备份完成。')
            f.close()
    except netmiko.exceptions.NetmikoTimeoutException:
        device_unreachable_issue_ip = print(ip + ' 网络不可达！')
        device_unreachable_issue_ips = open('备份设备的网络不可达ip列表-%s.txt'%(current_datetime),'a')
        device_unreachable_issue_ips.write('设备ip: %s网络不可达'%(ip) + '\n')
        device_unreachable_issue_ips.close()

#schedule.every().friday.at('06:00').do(back_config)
schedule.every(5).seconds.do(back_config)

while True:
    schedule.run_pending()

#centos后台运行python脚本
#nohup python 脚本文件名.py &

#centos后台停止python脚本
#kill $(pgrep 脚本文件名.py)