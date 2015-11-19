# -*- coding: utf-8 -*-
import lewei,time
from get_temp import get_cpu_temp,get_gpu_temp
'''
一个非常简单的demo，定时上传两个传感器数据,并不停的读取TCP反控连接的控制数据
作者：行知
邮件：lasoxygen@gmail.com
'''
sensorData = {}
def run():

    tempValue = 0 #温度

    lw = lewei.LeWeiLib("6706d916dadc496682ba2b3fabef4ead") #传入用户key
    #w.TcpControlInit("01") #初始化TCP反向控制连接,需传入网关号
    
    
    lasttime = time.time()
    while 1:
        time.sleep(10)
        #if ret:
        #    print "接收到TCP反向控制数据：",ret
            
        sensorData["raspi"] = get_cpu_temp()
        sensorData["raspi_gpu"] = get_gpu_temp()
        #用字典管理传感器，"bat","temp"是传感器名称，要和你在乐联网上的传感器名称一样
        tempValue += 1
        
        ret = lw.updateSensors("01", sensorData) #传入网关号及传感器数据
        if ret != -1:
            if ret["Successful"] == True:
                print u"上传传感器数据成功！Message：",ret["Message"]
            else:
                print u"上传传感器数据失败！Message：",ret["Message"]
        else:
            print "遇到错误，无法上传数据"
            

if __name__ == "__main__":
    run()
