#coding:utf-8
import os,sys
from models import Temp_Node
from datetime import datetime
from random import random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#如果已经在了，不要重复添加
if sys.path[0] != parentdir:
    sys.path.insert(0,parentdir)

from django.http import HttpResponse
from django.shortcuts import render 

from iot.echart import echart

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))
    #return HttpResponse(u"欢迎光临 !")

def add2(request,a,b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

#构造测试温度数据
def test_time(node_List,data_func):
    data = []
    for node in node_List:
        t = {}
        date = node.date
        t[u'date'] = date.isoformat()
        t[u'data'] = data_func(node)
        data.append(t)
    return data
@cache_page(60 * 1) # 秒数，这里指缓存 1 分钟，不直接写900是为了提高可读性
def home(request):
    string = u"我正在Django，用它来建网站"
    object_list = Temp_Node.objects.all().order_by('id')[:1000]
    t3 = Temp_Node()
    tt = echart()
    t = [0, 100, 0, 100, 12, 13, 10]
    tt.addSeries(u'temperature',test_time(object_list,lambda x:"%.1f"%(x.temperature)),isTime = True)
    tt.addSeries(u'humidity',test_time(object_list,lambda x:"%.1f"%(x.humidity)),isTime = True)
    tt.addSeries(u'flux',test_time(object_list,lambda x:"%.1f"%(x.l_flux)),isTime = True)
    
    
    #tt.addSeries(u'测试气温',t)
    #tt.addSeries(u'最低气温',t)
    #tt.addSeries(u'最高气温',t)
    #print tt.getSeries()
    return render(request, 'home.html', 
        {'string': string,
        "legend":tt.getLegend(),
        "series":tt.getSeries(),
        "formatter":tt.getFormatter(),
        "xAxis":tt.getXAxis(),
        })
