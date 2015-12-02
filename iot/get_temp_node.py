#!/usr/lib/python2.7/ python
# -*- coding: utf-8 -*-
import socket, traceback
from random import random
from math import sin,pi
from time import sleep
from math import cos
from copy import copy
from save_temp_node import save_temp_node
from binascii import b2a_hex as str2int
from binascii import a2b_hex as int2str
measure_struct = (
    (u'temperature',8),
    (u'humidity',8),
    (u'l_flux',16),
    (u'isOn',8),
)
'''
输入:收到的字符串 数据结构体
输出 tuple (name,data,bit_len)
'''
def message_decode(str_1,extera_struct = None):
    decode_list = map(lambda x: int(str2int(x),16),list(str_1))
    structs = (
        (u"type",16),
        (u"address",16),
    )
    if extera_struct:
        structs += extera_struct
    status_rst = []
    structs_l = list(structs)
    for item in structs_l:
        times = item[1]/8
        data = 0
        for bits in range(times):
            data |= decode_list.pop(0)<<(bits*8)
        status_rst.append((item[0],data,item[1]))
    return tuple(status_rst)

measure_struct_data = (
    (u"type",1,16),
    (u"address",2,16),
    (u'light_max',500,16),
    (u'duty_max',1000,16),
    (u'breathing_step',10,16),
)
'''
输入:准备输出的数据结构体 tuple (name,data,bit_len)
输出:完成编码的字符串
'''
def message_encode(structs):
    structs_l = list(structs)
    rst = ""
    for item in structs_l:
        item = list(item)
        times = item[2]/8
        data = ''
        for bits in range(times):
            data += chr(item[1]&0xff)
            item[1] >>= 8
        rst += data
    return rst

def message_display(data_struct):
    print '+-------------------+'
    for datas in data_struct:
        print u'|',datas[0],u":",datas[1],u"||",datas[2],"bits"
    print '+-------------------+'
port_in = 55554
port_out = 55555

if __name__ == "__main__":
    print "python UDP client test"
    print "Use Ctrl+C to break!"
    #UDP get IP address
    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s_in.bind(("",port_in))
    while(1):
        addr = s_in.recv(4096)
        decode_struct =  message_decode(addr,measure_struct)
        message_display(decode_struct)
        
        save_temp_node(decode_struct[0][1],decode_struct[1][1],decode_struct[2][1])
        
    s_in.close()
    
    '''
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = message_encode(measure_struct_data)
    s_out.sendto(t,("192.168.1.149", port_out))'''
