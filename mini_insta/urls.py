# mini_insta/urls.py
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView


# Only two pages, individual profile page and show all page
urlpatterns = [
  path('', ProfileListView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
  
]