# dadjokes/api/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomJokeAPIView),
    path('random', RandomJokeAPIView),
    path('jokes', JokeListAPIView),
    path('joke/<int:pk>', JokeDetailAPIView),
    path('pictures', PictureListAPIView),
    path('picture/<int:pk>', PictureDetailAPIView),
    path('random_picture', RandomPictureAPIView),
]