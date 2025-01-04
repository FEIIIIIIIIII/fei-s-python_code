#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   napalm.01.找出交换机端口up的mac.py
Time    :   2025/01/04 13:12:50
Author  :   afei 
Version :   python 3.11
'''

#暂不支持华为，以思科ios为例
from napalm import get_network_driver
import json
from getpass import getpass

ip = '192.168.235.2'
username = input('Username: ')
password = getpass('Password: ')

device = get_network_driver('ios')
SW = device(ip,username,password)
SW.open()
output = SW.get_interfaces()    #如果print(output)，数据类型为字典，影响阅读

print(json.dumps(output,indent=2))    #使用json()函数，2个空格缩进，将dict转换为带格式化的str打印输出，方便阅读和进行下面代码编写
'''
{
  "FastEthernet0/1": {
    "is enabled": false,
    "is up": false,
    "description": "",
    ""mac address": "00:23:34:2A:F6:40",
    "last flapped": -1.0,
    "mtu": 1500,
    "speed": 1000
    },
  "FatEthernet0/2": {
    "is enabled": true,
    "is up": true,
    "description": "",
    "mac address": "00:23:34:2A:F6:42",
    "last flapped": -1.0,
    "mtu": 1500,
    "speed": 1000
  }
}
使用json的子模块函数打印后，会发现上面是一个方便阅读的字典，这个字典的value也是一个字典。比如字典的第一个key是"FastEthernet0/1"，对应value是下面这个字典：
   {
    "is enabled": false,
    "is up": false,
    "description": "",
    ""mac address": "00:23:34:2A:F6:40",
    "last flapped": -1.0,
    "mtu": 1500,
    "speed": 1000
    }
'''

print('\n交换机%s下列端口的端口状态为up：\n' %(ip))    #%s对应的值是%(ip)，即192.168.235.2

for key,value in output.items():
    if value['is_up'] == True:
        print(key + 'MAC地址为' + value['mac_address'])