# dadjokes/api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random


@api_view(['GET', 'POST'])
def JokeListAPIView(request):
    '''Return all Jokes'''
    if request.method == 'GET':
        return Response(JokeSerializer(Joke.objects.all(), many=True).data)

    serializer = JokeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def RandomJokeAPIView(request):
    '''Return one random Joke'''

    joke = random.choice(Joke.objects.all())
    return Response(JokeSerializer(joke).data)


@api_view(['GET'])
def JokeDetailAPIView(request, pk):
    '''Return one joke by pk'''

    joke = Joke.objects.get(pk=pk)
    return Response(JokeSerializer(joke).data)



@api_view(['GET'])
def PictureDetailAPIView(request, pk):
    '''Return one picture by pk'''
    picture = Picture.objects.get(pk=pk)
    return Response(PictureSerializer(picture).data)


@api_view(['GET'])
def PictureListAPIView(request):
    '''Return all pictures'''
    return Response(PictureSerializer(Picture.objects.all(), many=True).data)



@api_view(['GET'])
def RandomPictureAPIView(request):
    '''Return one random picture'''

    picture = random.choice(Picture.objects.all())
    return Response(PictureSerializer(picture).data)