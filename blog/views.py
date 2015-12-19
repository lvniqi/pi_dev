# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from django.http import Http404
from django.views.generic.detail import DetailView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import models

from forms import ArticlePublishForm

from models import Article
#对于非管理员用户隐藏发布/编辑文章按钮
from django.contrib.admin.views.decorators import staff_member_required
#cache
from caching.base import CachingMixin, CachingManager, cached_method
#import mock
# This global call counter will be shared among all instances of an Addon.
#call_counter = mock.Mock()


class AdminRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(AdminRequiredMixin, cls).as_view(**initkwargs)
        print 'test'
        return staff_member_required(view)

class ArticlePublishView(AdminRequiredMixin,FormView):
    template_name = 'article_publish.html'
    form_class = ArticlePublishForm
    success_url = '/blog/'
    def form_valid(self, form):
        form.save(self.request.user.username)
        return super(ArticlePublishView, self).form_valid(form)

    
class ArticleListView(CachingMixin,models.Model,ListView):
    val = models.IntegerField()
    
    objects = CachingManager()
     
    class Meta:
        # without this, Postgres & SQLite return objects in different orders:
        ordering = ('pk',)
        
    template_name = 'blog_index.html'
    @cached_method
    def get_queryset(self, **kwargs):
        object_list = Article.objects.all().order_by('-'+'created')[:100]
        paginator = Paginator(object_list, 5)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            object_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            object_list = paginator.page(paginator.num_pages)
        for pos in range(len(object_list)):
            object_list[pos].tags = object_list[pos].tags.split()
        return object_list
        
class ArticleDetailView(CachingMixin,models.Model,DetailView):
    template_name = 'article_detail.html'
    def get_object(self, **kwargs):
        title = self.kwargs.get('title')
        try:
            article = Article.objects.get(title=title)
            article.views += 1
            article.save()
            article.tags = article.tags.split()
        except Article.DoesNotExist:
            raise Http404("Article does not exist")
        return article