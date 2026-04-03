# dadjokes/api/serializers.py
from rest_framework import serializers
from ..models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''for the joke model'''
    class Meta:
        # model and fields for JSON
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    '''for the picture model'''
    class Meta:
        # model and fields for Json
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']