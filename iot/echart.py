# -*- coding: utf-8 -*-
class echart:
    def __init__(self):
        self.type = "category"
        self.data = {}
        self.xAxis = []
        pass
    def addxAxis(self,xAxis):
        self.xAxis = xAxis
    
    def addSeries(self,title,data,isTime = None):
        #添加标准数据
        if isTime:
            #修改数据类型
            if self.type != "time":
                self.type = "time"
                self.data = {}
            d_t = []
            for item in data:
                time = u'new Date("%s")'%(item[u'date'])
                d_t.append((time,item[u'data']))
            self.data[title] = d_t
        #添加日期数据
        else:
            #修改数据类型
            if self.type != "category":
                self.type = "category"
                self.data = {}
            self.data[title] = data
            
    def series2Str(self,title):
        series = u"""
            {
                name:'%s',
                type:'line',
                data:%s,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }"""
        #标准数据
        if self.type == u"category":
            return series%(title,self.data[title])
        #日期数据
        elif self.type == u"time":
            length = len(self.data[title])
            data = "["
            for x in self.data[title]:
                data += u"["+x[0]+ u',' + str(x[1]) + u'],'
            data += u"]"
            return series%(title,data)
    def getSeries(self):
        result = u''
        for x in self.data:
            result += self.series2Str(x)+u','
        return u'['+result+u'],'
    def getLegend(self):
        result = u''
        for x in self.data:
            result += u"'"+x+u"',"
        return u'['+result+u'],'
    def getXAxis(self):
        #标准数据
        if self.type == u"category":
            return u"""type : 'category',
							boundaryGap : false,
							data : ['周一','周二','周三','周四','周五','周六','周日']
                    """
        #日期数据
        elif self.type == u"time":
            return u"""type : 'time',
                        splitNumber:10,
                    """
    def getFormatter(self):
        if self.type == "time":
            return u'''formatter : function (params) {
							var date = new Date(params.value[0]);
							data = date.getFullYear() + '-'
								   + (date.getMonth() + 1) + '-'
								   + date.getDate() + ' '
								   + date.getHours() + ':'
								   + date.getMinutes();
							return data + '<br/>'
								   + params.value[1];
						},'''
        else:
            return ''