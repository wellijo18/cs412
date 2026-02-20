from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
  '''a form to add a post to database'''
  image_url = forms.URLField(required=False, label="pic url")
  class Meta:
    '''assocaite this post with a profile from our database'''
    model = Post
    fields= ['caption']

