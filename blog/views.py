from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
import random
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW


from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW


# Create your views here.

class ShowAllViews(ListView):
    """defines a view class to show all blog articlez"""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)


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


# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user

        return super().form_valid(form)

    

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 


class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
        

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # create and return a URL:
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})
    


class UpdateArticleView(UpdateView):
    '''A view to update an Article and save it to the database.'''

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)
    
class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''

    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})
    

class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User


class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')