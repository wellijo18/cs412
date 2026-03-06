from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random
# Create your views here.

class ShowAllView(ListView):
  '''Define a view class to show all blog articles.'''
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
  '''Display a single article.'''
  model = Article
  template_name='blog/article.html'
  context_object_name = 'article'

class RandomArticleView(DetailView):
  '''Display a random article.'''
  model = Article
  template_name='blog/article.html'
  context_object_name = 'article'

  #methods
  def get_object(self):
    all_articles = Article.objects.all()
    article = random.choice(all_articles)
    return article


class CreateArticleView(LoginRequiredMixin, CreateView):
  '''a view to handle the creation of a new article'''
  form_class = CreateArticleForm
  template_name = 'blog/create_article_form.html'

  def get_login_url(self):
    return reverse('login')

  def form_valid(self, form):
    print(f'CreateArticleView.form_Valid(): {form.cleaned_data}')
    user = self.request.user
    print(f'CreateArticleView.form_Valid(): {user}')

    form.instance.user = user
    return super().form_valid(form)


class CreateCommentView(CreateView):
  form_class = CreateCommentForm
  template_name = 'blog/create_comment_form.html'

  def get_success_url(self):
    # return reverse('show_all')
    pk = self.kwargs['pk']
    return reverse('article', kwargs={'pk': pk})

  def form_valid(self, form):
    print(form.cleaned_data)
    pk = self.kwargs['pk']
    article = Article.objects.get(pk=pk)
    form.instance.article = article
    return super().form_valid(form)

  def get_context_data(self):
    '''return the dictionary of context variables for use in the template'''

    context = super().get_context_data()

    # find and add the article to the context data
    pk = self.kwargs['pk']
    article = Article.objects.get(pk=pk)

    # add tis artilce into the context dictionary
    context['article'] = article
    return context

class UpdateArticleView(UpdateView):
  model=Article
  form_class = UpdateArticleForm
  template_name = 'blog/update_article_form.html'

class DeleteCommentView(DeleteView):
  model = Comment
  template_name='blog/delete_comment_form.html'

  def get_success_url(self):
    pk = self.kwargs['pk']
    comment = Comment.objects.get(pk=pk)
    article = comment.article
    return reverse('article', kwargs={'pk':article.pk})

class UserRegistrationView(CreateView):
  template_name= 'blog/register.html'
  form_class = UserCreationForm
  model = User

  def get_success_url(self):
    return reverse('login')