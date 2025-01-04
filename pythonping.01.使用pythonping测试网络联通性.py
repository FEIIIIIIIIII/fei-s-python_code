#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   pythonping.01.使用pythonping测试网络联通性.py
Time    :   2025/01/04 12:50:10
Author  :   afei 
Version :   python 3.11
'''

from pythonping import ping

iplist = open('ip_list.txt')

for ip in iplist:
    result = ping(ip)
    if 'Reply from ' in str(result):
        print(ip + ' 网络可达')
    else:
        print(ip + ' 网络不可达')
iplist.close()