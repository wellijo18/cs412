# dadjokes/views.py
from django.views.generic import TemplateView, ListView, DetailView
from .models import Joke, Picture
import random

class RandomView(TemplateView):
    '''Show one random Joke and one random Picture'''
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = random.choice(Joke.objects.all())
        context['picture'] = random.choice(Picture.objects.all())
        return context


class ShowAllJokesView(ListView):
    '''Show all Jokes'''
    model = Joke
    template_name = 'dadjokes/all_jokes.html'
    context_object_name = 'jokes'


class SingleJokeView(DetailView):
    '''Show one Joke by primary key'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class ShowAllPicturesView(ListView):
    '''Show all Pictures'''
    model = Picture
    template_name = 'dadjokes/all_pictures.html'
    context_object_name = 'pictures'


class SinglePictureView(DetailView):
    '''Show one Picture by primary key'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'