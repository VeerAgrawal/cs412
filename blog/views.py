from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.

class ShowAllViews(ListView):
    """defines a view class to show all blog articlez"""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"


class ArticleView(DetailView):
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"



class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
