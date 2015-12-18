#!/usr/lib/python2.7/ python
# -*- coding: utf-8 -*-
import socket, traceback
from time import sleep
from save_temp_node import temperature_node
from com_message import com_message
from datetime import datetime    
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
    #print last
    message = com_message(2,1,measure_struct)
    last_date = last[3]
    last_data = list(last[4:])
    last_udate = True
    #print last_date
    while(1):
        (temperature,humidity,l_flux) = ([],[],[])
        for i in range(12):
            bit_datas = s_in.recv(4096)
            decode_struct =  message.decode(bit_datas)
            (temperature_t,humidity_t,l_flux_t) = decode_struct.getDatas(measure_struct_save)
            #print i,(temperature_t,humidity_t,l_flux_t)
            temperature.append(temperature_t)
            humidity.append(humidity_t)
            l_flux.append(l_flux_t)
            #save_temp_node(decode_struct[2][1],decode_struct[3][1],decode_struct[4][1])
        def __get_mid(data_list):
            data_len_d2 = len(data_list)/2
            data_list.sort()
            return 1.0*(data_list[data_len_d2-1]+data_list[data_len_d2]+data_list[data_len_d2+1])/3
        new_data = map(lambda x:__get_mid(x),(temperature,humidity,l_flux))
        if last_data[:2] != new_data[:2] or abs(last_data[2]-new_data[2])>50:
            if not last_udate:
                last_udate = True
                t_node.save_temp_node(last_data[0],last_data[1],last_data[2],last_date)
            print "update!",last_data,new_data
            t_node.save_temp_node(new_data[0],new_data[1],new_data[2])
            last_data = new_data
        else:
            print "un change",last_data,new_data
            last_udate = False
        last_date = datetime.utcnow().__str__()
        
    s_in.close()
    
    '''
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = message_encode(measure_struct_data)
    s_out.sendto(t,("192.168.1.149", port_out))'''
