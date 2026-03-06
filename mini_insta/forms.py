# mini_insta/forms.py

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
  '''a form to add a post to database'''
  
  class Meta:
    '''associate this post with a profile from our database'''
    model = Post
    fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
  '''a form to update a profile'''
  class Meta:
    model= Profile
    fields = ['username', 'display_name', 'profile_image_url', 'bio_text']

class CreateProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['username', 'display_name', 'profile_image_url', 'bio_text']