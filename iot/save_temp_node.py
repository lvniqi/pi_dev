# -*- coding: utf-8 -*-
import os
import sqlite3
from datetime import datetime    
import com_meassage
#温度节点
class temperature_node:
    
    def __init__(self):
        self.path = self.getdir()
        self.cx = sqlite3.connect(self.path)
        self.cu = self.cx.cursor()
    def getdir(self):
        '''得到数据库地址'''
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/')+'/pi_dev/db.sqlite3'
    def get_last_temp_node(self,node,tags = None):
        '''根据node 和 tag 获取上次的存储数据'''
        cu2 = self.cu.execute("select * from home_temp_node where node = '%s'"%str(node))
        return cu2.fetchall()[-1]
    def save_temp_node(self,temperature,humidity,l_flux,date = None):
        '''保存数据'''
        if not date:
            date = datetime.today().__str__()
        
        cu2 = self.cu.execute("select * from home_temp_node")
        num = cu2.fetchall()[-1][0]
        insert_data = (num+1,u'test',u'test',date,
                           temperature,
                           humidity,
                           l_flux)
        self.cu.execute("insert into home_temp_node values (?,?,?,?,?,?,?)",insert_data)
        self.cx.commit()
    
    
        
if __name__ == "__main__":
    t = temperature_node()
    print t.get_last_temp_node(u"test")
    t.save_temp_node(1,2,3)
    print t.get_last_temp_node(u"test")