#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render 
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))
    #return HttpResponse(u"欢迎光临 !")

def add2(request,a,b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

def home(request):
    string = u"我正在Django，用它来建网站"
    return render(request, 'home.html', {'string': string})
