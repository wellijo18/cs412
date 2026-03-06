#mini_insta/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Follow, Like
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import random
# Create your views here.
# create listview for show all page


class AuthForMixin(LoginRequiredMixin):
  def get_login_url(self):
    return reverse('login')

  def get_user_profile(self):
    return Profile.objects.get(user=self.request.user)


class ProfileListView(ListView):
  '''Define a view class to show all profile articles.'''
  model = Profile
  template_name = "mini_insta/show_all_profiles.html"
  context_object_name = "profiles"

# create single profile view page for clicked on
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['my_profile'] = Profile.objects.get(user=self.request.user)
        return context
# create single post view page when post done being created or clicked on
class PostDetailView(DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            context['my_profile'] = my_profile
            context['user_likes_post'] = Like.objects.filter(profile=my_profile, post=self.object).exists()
        return context

# used for creation of post, auth for makeing sure logged in
class CreatePostView(AuthForMixin, CreateView):

  form_class = CreatePostForm
  template_name = 'mini_insta/create_post_form.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['profile'] = Profile.objects.get(user=self.request.user)
    return context

  def form_valid(self, form):
    profile = Profile.objects.get(user=self.request.user)
    form.instance.profile = profile
    self.object = form.save()

    files = self.request.FILES.getlist('images')
    for file in files:
      Photo.objects.create(post=self.object, image_file=file)

    return super().form_valid(form)

  def get_success_url(self):
    return reverse('post', kwargs={'pk': self.object.pk})

# updateprofile view, auth for makeing sure logged in
class UpdateProfileView(AuthForMixin, UpdateView):

  model = Profile
  form_class = UpdateProfileForm
  template_name = 'mini_insta/update_profile_form.html'
  context_object_name = 'profile'

  def get_object(self):
    return Profile.objects.get(user=self.request.user)

  def get_success_url(self):
    return reverse('my_profile')
# for deleteing posts, auth for makeing sure logged in
class DeletePostView(AuthForMixin, DeleteView):
  '''view to delete a psot'''
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
# for updating posts, auth for makeing sure logged in
class UpdatePostView(AuthForMixin, UpdateView):
  '''view to update a post'''
  model = Post
  form_class = CreatePostForm
  template_name = 'mini_insta/update_post_form.html'
  context_object_name = 'post'

  def get_success_url(self):
    return reverse('post', kwargs={'pk': self.object.pk})
# showing followers of profile
class ShowFollowersDetailView(DetailView):
  '''view to show followers of profile'''

  model = Profile
  template_name = 'mini_insta/show_followers.html'
  context_object_name = 'profile'
# showing who user following lsit
class ShowFollowingDetailView(DetailView):
  '''view to show profiles profile follows'''

  model = Profile
  template_name = 'mini_insta/show_following.html'
  context_object_name = 'profile'
# view to see feed of posts from profiles followed
class PostFeedListView(AuthForMixin, ListView):

  model = Post
  template_name = 'mini_insta/show_feed.html'
  context_object_name = 'posts'

  def get_queryset(self):
    profile = Profile.objects.get(user=self.request.user)
    return profile.get_post_feed()
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['profile'] = Profile.objects.get(user=self.request.user)
    return context
# for search feature
class SearchView(AuthForMixin, ListView):

  template_name = 'mini_insta/search_results.html'

  def dispatch(self, request, *args, **kwargs):
    if 'query' not in request.GET:
      return render(request, 'mini_insta/search.html')
    return super().dispatch(request, *args, **kwargs)
  def get_queryset(self):
    query = self.request.GET.get('query')
    return Post.objects.filter(caption__icontains=query)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    query = self.request.GET.get('query')
    posts = Post.objects.filter(caption__icontains=query)

    all_profiles = Profile.objects.all()
    matching_profiles = []
    for p in all_profiles:
      if query.lower() in p.username.lower() or query.lower() in p.display_name.lower() or query.lower() in p.bio_text.lower():
        matching_profiles.append(p)

    context['query'] = query
    context['posts'] = posts
    context['profiles'] = matching_profiles

    return context
# auth for makeing sure logged in, for when logged in view profile
class DaProfileView(AuthForMixin, DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
# for creating profiel need to update database wit it
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_profile')
# view to connect logged in account to follow, auth for makeing sure logged in
class FollowProfileView(AuthForMixin, TemplateView):
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_user_profile()
        if my_profile != other_profile:
            Follow.objects.get_or_create(follower_profile=my_profile, profile=other_profile)
        return redirect('profile', pk=other_profile.pk)
# view that removes follower if user wants to unfollow and auth for makeing sure logged in
class RemoveFollowProfileView(AuthForMixin, TemplateView):
    template_name = None
    def dispatch(self, request, *args, **kwargs):
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_user_profile()
        Follow.objects.filter(follower_profile=my_profile, profile=other_profile).delete()
        return redirect('profile', pk=other_profile.pk)
# connects user to like for post, auth for makeing sure logged in 
class LikePostView(AuthForMixin, TemplateView):
    template_name = None
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_user_profile()
        if my_profile != post.profile:
            Like.objects.get_or_create(profile=my_profile, post=post)
        return redirect('post', pk=post.pk)
# remove da user like from post, auth for makeing sure logged in
class RemoveLikePostView(AuthForMixin, TemplateView):
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_user_profile()
        Like.objects.filter(profile=my_profile, post=post).delete()
        return redirect('post', pk=post.pk)