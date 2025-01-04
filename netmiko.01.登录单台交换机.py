#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   netmiko.01.登录单台交换机.py
Time    :   2025/01/04 13:11:34
Author  :   afei 
Version :   python 3.11
'''

#导入netmiko的子模块函数ConnectHandler给当前代码脚本
from netmiko import ConnectHandler

#定义交换机厂商和登录信息
device = {'device_type':'huawei',
          'ip':'192.168.235.2',
          'username':'test',
          'password':'test'}

#通过**关键字参数将device字典的内容，传递给ConnectHandler()函数
connect = ConnectHandler(**device)
print('已经成功登录交换机' + device['ip'])

#建立配置命令集
config_commands = ['vlan 2','interface Vlanif 2','ip address 1.1.1.1 30']

#将配置命令集config_commands内容，传递给ConnectHandler的函数子模块send_config_set()，配置完毕后将配置信息赋值给output用于打印
output = connect.send_config_set(config_commands)
print(output)

#将配置单条配置命令，传递给ConnectHandler的函数子模块send_command，配置完毕后将配置信息赋值给result用于打印
result = connect.send_command('display current-configuration interface Vlanif 2')
print(result)