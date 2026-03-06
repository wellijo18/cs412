# mini_insta/urls.py
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, PostFeedListView, SearchView, DaProfileView, CreateProfileView, FollowProfileView, RemoveFollowProfileView, LikePostView, RemoveLikePostView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
  path('', ProfileListView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
  path('post/<int:pk>', PostDetailView.as_view(), name='post'),
  path('profile/create_post', CreatePostView.as_view(), name='create_post'),
  path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
  path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
  path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
  path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
  path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
  path('profile/feed', PostFeedListView.as_view(), name='show_postfeed'),
  path('profile/search', SearchView.as_view(), name='search'),
  path('profile', DaProfileView.as_view(), name='my_profile'),
  path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
  path('logout_confirmation/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),
  path('create_profile', CreateProfileView.as_view(), name='create_profile'),
  path('profile/<int:pk>/follow', FollowProfileView.as_view(), name='follow_profile'),
  path('profile/<int:pk>/remove_follow', RemoveFollowProfileView.as_view(), name='remove_follow_profile'),
  path('post/<int:pk>/like', LikePostView.as_view(), name='like_post'),
  path('post/<int:pk>/remove_like', RemoveLikePostView.as_view(), name='remove_like_post'),
]