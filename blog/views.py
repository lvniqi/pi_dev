# Create your views here.
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from django.http import Http404
from django.views.generic.detail import DetailView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F

from forms import ArticlePublishForm

from models import Article

def blog_index(request):
    context = {
        'test': 'just for test.',
        'welcome': 'hello world.'
    }
    return render(request, 'blog_index.html', context)
    
class ArticlePublishView(FormView):
    template_name = 'article_publish.html'
    form_class = ArticlePublishForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.save(self.request.user.username)
        return super(ArticlePublishView, self).form_valid(form)
        
class ArticleListView(ListView):
    template_name = 'blog_index.html'

    def get_queryset(self, **kwargs):
        object_list = Article.objects.all().order_by('created')[:100]
        paginator = Paginator(object_list, 10)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            object_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            object_list = paginator.page(paginator.num_pages)
        return object_list
        
class ArticleDetailView(DetailView):
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