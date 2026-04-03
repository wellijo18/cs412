# dadjokes/models.py

from django.db import models
from django.urls import reverse

# Create your models here.
class Joke(models.Model):
    '''Encapsulate dad joke made by a user'''
    text = models.TextField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of joke'''
        return f'Joke by {self.name}: {self.text[:50]}'

    def get_absolute_url(self):
        '''Return the URL to display instance of joke'''
        return reverse('joke', kwargs={'pk': self.pk})


class Picture(models.Model):
    '''Encapsulate funny picture or GIF provided by a user'''
    image_url = models.URLField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of picture'''
        return f'Picture by {self.name}: {self.image_url}'

    def get_absolute_url(self):
        '''Return the URL to display instance picture'''
        return reverse('picture', kwargs={'pk': self.pk})