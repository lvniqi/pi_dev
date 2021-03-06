#!/usr/bin/env python
# coding=utf-8

import datetime
import re
import markdown
import os
import qrcode

from django import forms

from models import Article

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dic_dir =  parentdir.replace('\\','/')+'/static/qrcode/'

class ArticlePublishForm(forms.Form):
    title = forms.CharField(
        label=u'文章标题',
        max_length=50,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': u'文章标题'}),
        )

    content = forms.CharField(
        label=u'内容',
        min_length=10,
        widget=forms.Textarea(),
        )

    tags = forms.CharField(
        label=u'标签',
        max_length=30,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': u'文章标签，以空格进行分割'}),
        )

    def save(self, username, article=None):
        cd = self.cleaned_data
        title = cd['title']
        title_zh = title
        now = datetime.datetime.now()
        content_md = cd['content']
        content_html = markdown.markdown(content_md, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        re_title = '<h1>(.+)</h1>'
        data = content_html.split('\n')
        for line in data:
            title_info = re.findall(re_title, line)
            if title_info:
                title_zh = title_info[0]
                data.remove(line)
                data = map(lambda x:x+"\n",data)
                content_html = "".join(data)
                
                break
        url = '/article/%s' % (title)
        real_dir = dic_dir+title+'.png'
        if os.path.exists(real_dir):
            print "file exists!"
        else:
            img = qrcode.make("http://lvniqi.f3322.org/blog"+url)
            img.save(real_dir)
            
        tags = cd['tags']
        if article:
            article.url = url
            article.title = title
            article.title_zh = title_zh
            article.content_md = content_md
            article.content_html = content_html
            article.tags = tags
            article.updated = now
        else:
            article = Article(
                url=url,
                title=title,
                title_zh=title_zh,
                author=username,
                content_md=content_md,
                content_html=content_html,
                tags=tags,
                views=0,
                created=now,
                updated=now)
        article.save()