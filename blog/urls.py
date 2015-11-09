from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'blog.views.blog_index', name='blog_index'),
]