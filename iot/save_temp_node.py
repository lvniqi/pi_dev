from os import getcwd
import sqlite3
from datetime import datetime

def getdir():
    dir = getcwd()
    return dir[:dir.rindex('\\')]+'\\pi_dev\\db.sqlite3'

def save_temp_node(temperature,humidity,l_flux):
    cx = sqlite3.connect(getdir())
    cu=cx.cursor()
    cu2 = cu.execute("select * from home_temp_node")
    num = cu2.fetchall()[-1][0]
    insert_data = (num+1,u'test',u'test',datetime.today().__str__(),
                       temperature,
                       humidity,
                       l_flux)
    cu.execute("insert into home_temp_node values (?,?,?,?,?,?,?)",insert_data)
    cx.commit()
if __name__ == "__main__":
    save_temp_node(1,2,3)