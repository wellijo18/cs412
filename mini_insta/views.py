from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
import random
# Create your views here.

class ProfileListView(ListView):
  '''Define a view class to show all blog articles.'''
  model = Profile
  template_name = "mini_insta/show_all_profiles.html"
  context_object_name = "profiles"

class ProfileDetailView(DetailView):
  '''Display a single article.'''
  model = Profile
  template_name='mini_insta/show_profile.html'
  context_object_name = 'profile'

