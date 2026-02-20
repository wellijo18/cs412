from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
import random
# Create your views here.

class ShowAllView(ListView):
  '''Define a view class to show all blog articles.'''
  model = Article
  template_name = "blog/show_all.html"
  context_object_name = "articles"

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


class CreateArticleView(CreateView):
  '''a view to handle the creation of a new article'''
  form_class = CreateArticleForm
  template_name = 'blog/create_article_form.html'

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


