# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print parentdir
sys.path.insert(0,parentdir)
from iot.get_temp import get_status as get_temp

WECHAT_TOKEN = 'aqweczckahiqbfaksjdhuwqdlvniqi'
AppID = 'wx93690ae114779c99'
AppSecret = '45a654166db25633d6e708baeb947d35'

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
 
        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
 
        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")
 
 
    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')
 
    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '功能':
            reply_text = (
                    '目前支持的功能：\n1. 关键词后面加上【教程】两个字可以搜索教程，'
                    '比如回复 "Django 后台教程"\n'
                    '2. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'
                    '还有更多功能正在开发中哦 ^_^\n'
                    '【<a href="http://www.ziqiangxuetang.com">自强学堂手机版</a>】'
                )
        elif content.endswith('教程'):
            reply_text = '您要找的教程如下：'
	elif content.endswith('温度'):
            reply_text = get_temp()
        else:
            reply_text = content
        response = wechat_instance.response_text(content=reply_text)
    elif isinstance(message, VoiceMessage):
        response = wechat_instance.response_text(content=u'语音信息')
    elif isinstance(message, ImageMessage):
        response = wechat_instance.response_text(content=u'图片信息')
    elif isinstance(message, VideoMessage):
        response = wechat_instance.response_text(content=u'视频信息')
    elif isinstance(message, LinkMessage):
        response = wechat_instance.response_text(content=u'链接信息')
    elif isinstance(message, LocationMessage):
        response = wechat_instance.response_text(content=u'地理位置信息')
    elif isinstance(message, EventMessage):  # 事件信息
        if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                response = wechat_instance.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
            else:
                response = wechat_instance.response_text(content=u'普通关注事件')
        elif message.type == 'unsubscribe':
            response = wechat_instance.response_text(content=u'取消关注事件')
        elif message.type == 'scan':
            response = wechat_instance.response_text(content=u'用户已关注时的二维码扫描事件')
        elif message.type == 'location':
            response = wechat_instance.response_text(content=u'上报地理位置事件')
        elif message.type == 'click':
            response = wechat_instance.response_text(content=u'自定义菜单点击事件')
        elif message.type == 'view':
            response = wechat_instance.response_text(content=u'自定义菜单跳转链接事件')
        elif message.type == 'templatesendjobfinish':
            response = wechat_instance.response_text(content=u'模板消息事件')
    return HttpResponse(response, content_type="application/xml")
