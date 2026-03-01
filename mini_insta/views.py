#mini_insta/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm
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
# create single post view page when post done being created or clicked on
class PostDetailView(DetailView):
  '''Display a single article.'''
  model = Post
  template_name='mini_insta/show_post.html'
  context_object_name = 'post'

# used for creation of post
class CreatePostView(CreateView):
  '''a view to handle the creation of a new post'''

  form_class = CreatePostForm
  template_name = 'mini_insta/create_post_form.html'
  def get_success_url(self):
    pk = self.kwargs['pk']
    return reverse('post', kwargs={'pk': self.object.pk})
  # used for passing context cariables
  def get_context_data(self, **kwargs):
    '''return the dictionary of context variables'''
    context = super().get_context_data(**kwargs)

    #find and add the post to context data
    pk = self.kwargs['pk']
    profile = Profile.objects.get(pk=pk)
    context['profile'] = profile
    return context

  def form_valid(self, form):
    # attach post to profile
    pk = self.kwargs['pk']
    form.instance.profile_id = pk

    # save post
    self.object = form.save()

    # get uploaded files
    files = self.request.FILES.getlist('images')

    # create Photo objects
    for file in files:
        Photo.objects.create(post=self.object, image_file=file)

    return super().form_valid(form)


class UpdateProfileView(UpdateView):
  '''view to update a profile'''

  model = Profile
  form_class = UpdateProfileForm
  template_name = 'mini_insta/update_profile_form.html'
  context_object_name = 'profile'

  def get_success_url(self):
    return reverse('profile', kwargs={'pk': self.object.pk})

class DeletePostView(DeleteView):
  '''view to delete a post'''

  model = Post
  template_name = 'mini_insta/delete_post_form.html'
  context_object_name = 'post'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    post = self.object
    profile = post.profile

    context['post'] = post
    context['profile'] = profile
    return context

  def get_success_url(self):
    return reverse('profile', kwargs={'pk': self.object.profile.pk})

class UpdatePostView(UpdateView):
  '''view to update a post'''

  model = Post
  form_class = CreatePostForm
  template_name = 'mini_insta/update_post_form.html'
  context_object_name = 'post'

  def get_success_url(self):
    return reverse('post', kwargs={'pk': self.object.pk})

class ShowFollowersDetailView(DetailView):
  '''view to show followers of profile'''

  model = Profile
  template_name = 'mini_insta/show_followers.html'
  context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
  '''view to show profiles profile follows'''

  model = Profile
  template_name = 'mini_insta/show_following.html'
  context_object_name = 'profile'