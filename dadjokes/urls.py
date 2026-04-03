# dadjokes/urls.py

from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', RandomView.as_view(), name='random'),
    path('random', RandomView.as_view(), name='random'),
    path('jokes', ShowAllJokesView.as_view(), name='jokes'),
    path('joke/<int:pk>', SingleJokeView.as_view(), name='joke'),
    path('pictures', ShowAllPicturesView.as_view(), name='pictures'),
    path('picture/<int:pk>', SinglePictureView.as_view(), name='picture'),
    path('api/', include('dadjokes.api.urls')),
]