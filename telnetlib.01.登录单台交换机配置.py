#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File    :   telnetlib.01.登录单台交换机配置.py
Time    :   2025/01/04 12:47:53
Author  :   afei 
Version :   python 3.11
'''

#请注意！！！python3.13已经没有内置telnetlib模块
import telnetlib

ip = '192.168.235.2'
username = 'test'
password = 'test'

tn = telnetlib.Telnet(ip)

tn.read_until(b'Username: ')
tn.write(username.encode('ascii') + b'\n')
tn.read_until(b'Password: ')
tn.write(password.encode('ascii') + b'\n')

print('已经成功登录交换机' + ip)
tn.write(b'system-view\n')
tn.write(b'inter loopback 0\n')
tn.write(b'ip address 1.1.1.1 32\n')
tn.write(b'quit\n')
tn.write(b'quit\n')
tn.write(b'save\n')
tn.write(b'y\n')
tn.write(b'quit\n')

#telnetlib必须完全退出telnet登录，才能使用read_all()函数打印输出
output = tn.read_all().decode('ascii')
print(output)

#如果你不想退出交换机也想打印输出配置了什么，可以使用read_very_eager()函数
#output = tn.read_very_eager().decode('ascii')
#print(output)