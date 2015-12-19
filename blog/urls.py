from django.conf.urls import url
from views import ArticlePublishView,ArticleListView,ArticleDetailView
#from django.views.decorators.cache import cache_page
urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='blog_index'),
    #url(r'^$', 'blog.views.blog_index', name='blog_index'),
    url(r'^article/publish$', ArticlePublishView.as_view(), name='article_publish'),
    url(r'^article/(?P<title>\S+)$', ArticleDetailView.as_view(), name='article_detail'),
]