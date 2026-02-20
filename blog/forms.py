from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
  '''a form to add an article to database'''
  class Meta:
    '''assocaite this form with a model form our database'''
    model = Article
    fields = ['author', 'title', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['author', 'text']
