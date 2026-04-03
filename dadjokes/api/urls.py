# dadjokes/api/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomJokeAPIView.as_view()),
    path('random', RandomJokeAPIView.as_view()),
    path('jokes', JokeListAPIView.as_view()),
    path('joke/<int:pk>', JokeDetailAPIView.as_view()),
    path('pictures', PictureListAPIView.as_view()),
    path('picture/<int:pk>', PictureDetailAPIView.as_view()),
    path('random_picture', RandomPictureAPIView.as_view()),
]