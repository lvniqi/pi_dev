#coding:utf-8
import os,sys
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
def test_time():
    data = []
    for x in range(1,10):
        data.append(
            {
                u'year':2014,
                u'month':10,
                u'day':x,
                u'hour':12,
                u'minute':12,
                u'second':1,
                u'data':x
            }
        )
    return data
def home(request):
    string = u"我正在Django，用它来建网站"
    tt = echart()
    t = [0, 100, 0, 100, 12, 13, 10]
    tt.addSeries(u'测试温度数据',test_time(),isTime = True)
    #tt.addSeries(u'测试气温',t)
    #tt.addSeries(u'最低气温',t)
    #tt.addSeries(u'最高气温',t)
    print tt.getSeries()
    return render(request, 'home.html', 
        {'string': string,
        "legend":tt.getLegend(),
        "series":tt.getSeries(),
        "formatter":tt.getFormatter(),
        "xAxis":tt.getXAxis(),
        })
