# -*- coding: utf-8 -*-
from binascii import b2a_hex as str2int
from binascii import a2b_hex as int2str
from copy import deepcopy

measure_struct_data = (
    (u'light_max',16,500),
    (u'duty_max',16,1000),
    (u'breathing_step',16,10),
)

class com_message:
    
    __base_struct = (
        (u"type",16),
        (u"address",16),
    )
    def __init__(self,type = 0,address = 0,structs = None):
        self.types = map(lambda struct:struct[0],com_message.__base_struct)
        self.type2data = dict(map(lambda type,name:(type[0],name),com_message.__base_struct,(type,address)))
        self.type2len = dict(com_message.__base_struct)
        if structs:
            self.addStructs(structs)
    def addPos(self,type,pos=None):
        '''添加一个数据类型的位置'''
        if(pos) == None:
            self.types.append(type)
        else:
            self.types = self.types[:pos][type,]+self.types[pos:]
    def addStruct(self,type,len=None,data = None,pos=None):
        '''添加一个数据类型'''
        self.addPos(type,pos)
        self.type2data[type] = data
        self.type2len[type] = len
    def removeStruct(self,type):
        '''删除一个数据类型'''
        self.type2data.pop(type)
        self.type2len.pop(type)
        self.types.remove(type)
    def addStructs(self,structs):
        '''结构体 tuple (name,bit_len,data,pos)'''
        '''添加多个数据类型'''
        def __addOne(x):
            #如果没有data pos选项
            if not x[3:] :
                x += (None,None)
            self.addStruct(x[0],x[1],x[2],x[3])
        for x in structs:
            __addOne(x)
    def addData(self,type,data):
        '''设置数据'''
        if type in self.types:
            self.type2data[type] = data
    def getData(self,type):
        '''得到数据'''
        return self.type2data[type]
    def getDatas(self,types):
        '''得到数据组'''
        return tuple(map(lambda type:self.getData(type),types))
    def encode(self):
        '''
        输入:准备输出的数据结构体 tuple (name,num,data,bit_len)
        输出:完成编码的字符串
        '''
        rst = ""
        for type in self.types:
            times = self.type2len[type]/8
            data = self.type2data[type]
            data2str = ''
            for bits in range(times):
                data2str += chr(data&0xff)
                data >>= 8
            rst += data2str
        return rst
    def decode(self,str_1):
        '''
        输入:收到的字符串
        输出 com_message
        '''
        decode_list = map(lambda x: int(str2int(x),16),list(str_1))
        t = deepcopy(self)
        for type in t.types:
            times = t.type2len[type]/8
            data = 0
            for bits in range(times):
                data |= decode_list.pop(0)<<(bits*8)
            t.addData(type,data)
        head = map(lambda x:x[0],com_message.__base_struct)
        #if t.getDatas(head) == self.getDatas(head):
        return t
        #else:
        #    return None
    def __str__(self):
        rst = ""
        rst += '+-------------------+\r\n'
        for type in self.types:
            rst +=  str(type)+u": "
            rst +=  str(self.type2data[type])+u"|| "
            rst +=  str(self.type2len[type])+"bits\r\n"
        rst += '+-------------------+\r\n'
        return rst
    def display(self):
        '''
        输入:无
        输出:无
        显示:消息内容 
        '''
        print self.__str__()
if __name__ == "__main__":
    t = com_message(1,2,measure_struct_data)
    str_1 =  t.encode()
    tt = t.decode(str_1)
    t.display()
    tt.display()