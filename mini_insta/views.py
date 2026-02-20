#mini_insta/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from django.urls import reverse
from .forms import CreatePostForm
import random
# Create your views here.
# create listview for show all page
class ProfileListView(ListView):
  '''Define a view class to show all blog articles.'''
  model = Profile
  template_name = "mini_insta/show_all_profiles.html"
  context_object_name = "profiles"

# create single profile view page for clicked on
class ProfileDetailView(DetailView):
  '''Display a single article.'''
  model = Profile
  template_name='mini_insta/show_profile.html'
  context_object_name = 'profile'

class PostDetailView(DetailView):
  '''Display a single article.'''
  model = Post
  template_name='mini_insta/show_post.html'
  context_object_name = 'post'

class CreatePostView(CreateView):
  '''a view to handle the creation of a new post'''

  form_class = CreatePostForm
  template_name = 'mini_insta/create_post_form.html'
  def get_success_url(self):
    pk = self.kwargs['pk']
    return reverse('post', kwargs={'pk': self.object.pk})

  def get_context_data(self, **kwargs):
    '''return the dictionary of context variables'''
    context = super().get_context_data(**kwargs)

    #find and add the post to context data
    pk = self.kwargs['pk']
    profile = Profile.objects.get(pk=pk)
    context['profile'] = profile
    return context

  def form_valid(self,form):
    pk = self.kwargs['pk']
    form.instance.profile_id = pk
    self.object = form.save()
    image_url = form.cleaned_data.get('image_url')

    if image_url:
        Photo.objects.create(post=self.object, image_url=image_url)
    return super().form_valid(form)
