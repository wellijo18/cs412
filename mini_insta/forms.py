# mini_insta/forms.py

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
  '''a form to add a post to database'''
  
  class Meta:
    '''associate this post with a profile from our database'''
    model = Post
    fields = ['caption']