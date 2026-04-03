# dadjokes/api/views.py

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random


@method_decorator(csrf_exempt, name='dispatch')
class JokeListAPIView(generics.ListCreateAPIView):
    '''Return all Jokes'''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class RandomJokeAPIView(APIView):
    '''Return one random Joke'''
    def get(self, request):
        joke = random.choice(Joke.objects.all())
        serializer = JokeSerializer(joke)

        return Response(serializer.data)


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''Return one Joke by pk'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer



class PictureDetailAPIView(generics.RetrieveAPIView):
    '''Return one Picture by pk'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureListAPIView(generics.ListAPIView):
    '''Return all Pictures'''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(APIView):
    '''Return one random Picture'''
    def get(self, request):
        picture = random.choice(Picture.objects.all())
        serializer = PictureSerializer(picture)
        
        return Response(serializer.data)