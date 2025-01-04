#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   napalm.03.用napalm对比在线设备的配置差异.py
Time    :   2025/01/04 13:11:40
Author  :   afei 
Version :   python 3.11
'''

#暂不支持华为设备，本脚本代码以思科设备为例。
#前提需要在思科设备开启SCP开启命令如下：
'''
S1#conf ter
S1(config)#ip scp server enable
S1(config)#end
S1#
'''
#然后在python主机上创建对比交换机的配置文件.cfg，如：
'''
[root@localhost test]#vi napalm_config.cfg
line vty 5 15
transport input all
login all
'''

from napalm import get_network_driver
from getpass import getpass

ip = '192.168.235.2'
username = input('Username: ')
password = getpass('Password: ')

device = get_network_driver('ios')
SW = device(ip,username,password)
SW.open()

#load_merge_candidate()函数调用编辑好的配置文件napalm_config.cfg
SW.load_merge_candidate(filename='napalm_config.cfg')

differences = SW.compare_config()
print(differences)

#对比后，如果交换机缺失了配置，脚本文件会输出带+的命令
# 如：+transport input all,意思是交换机上没有配置这条命令