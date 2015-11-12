from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pi_dev.views.home', name='home'),
    # url(r'^pi_dev/', include('pi_dev.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$','wechat.views.index',name = 'home'),
    url(r'^$', 'home.views.home', name='home'),
    url(r'^add/$','home.views.add',name = 'add'),
    url(r'^add/(\d+)/(\d+)/$', 'wechat.views.add2', name='add2'),
    # blog
    url(r'^blog/', include('blog.urls')),
    # wechat
    url(r'^wechat/$','wechat.views.wechat',name = 'wechat'),
)
