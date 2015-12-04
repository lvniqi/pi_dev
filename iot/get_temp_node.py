#!/usr/lib/python2.7/ python
# -*- coding: utf-8 -*-
import socket, traceback
from time import sleep
from save_temp_node import temperature_node
from com_message import com_message

measure_struct = (
        (u'temperature',8),
        (u'humidity',8),
        (u'l_flux',16),
        (u'isOn',8),
    )

measure_struct_data = (
    (u"type",1,16),
    (u"address",2,16),
    (u'light_max',500,16),
    (u'duty_max',1000,16),
    (u'breathing_step',10,16),
)
measure_struct_save = ('temperature','humidity','l_flux')


port_in = 55554
port_out = 55555

if __name__ == "__main__":
    print "python UDP client test"
    print "Use Ctrl+C to break!"
    #UDP get IP address
    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s_in.bind(("",port_in))
    t_node = temperature_node()
    last = t_node.get_last_temp_node('test')
    print last
    message = com_message(2,1,measure_struct)
    while(1):
        (temperature,humidity,l_flux) = ([],[],[])
        for i in range(10):
            bit_datas = s_in.recv(4096)
            decode_struct =  message.decode(bit_datas)
            (temperature_t,humidity_t,l_flux_t) = decode_struct.getDatas(measure_struct_save)
            print i,(temperature_t,humidity_t,l_flux_t)
            temperature.append(temperature_t)
            humidity.append(humidity_t)
            l_flux.append(l_flux_t)
            #save_temp_node(decode_struct[2][1],decode_struct[3][1],decode_struct[4][1])
        def __get_mid(data_list):
            data_len_d2 = len(data_list)/2
            data_list.sort()
            return 1.0*(data_list[data_len_d2-1]+data_list[data_len_d2]+data_list[data_len_d2+1])/3
        print map(lambda x:__get_mid(x),(temperature,humidity,l_flux))

    s_in.close()
    
    '''
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = message_encode(measure_struct_data)
    s_out.sendto(t,("192.168.1.149", port_out))'''
