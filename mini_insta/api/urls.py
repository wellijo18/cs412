# mini_insta/api/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPIView),
    path('profiles/', ProfileListAPIView),
    path('profile/<int:pk>/', ProfileDetailAPIView),
    path('profile/<int:pk>/posts/', ProfilePostsAPIView),
    path('profile/<int:pk>/feed/', ProfileFeedAPIView),
    path('profile/<int:pk>/create_post/', CreatePostAPIView),
]