# mini_insta/api/serializers.py
from rest_framework import serializers
from ..models import Profile, Post, Photo

class MIPhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image', 'timestamp']

    def get_image(self, obj):
        return obj.get_image_url()

class MIPostSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    class Meta:
        model = Post

        fields = ['id', 'caption', 'timestamp', 'photos']

    def get_photos(self, obj):
        return MIPhotoSerializer(obj.get_all_photos(), many=True).data

class MIProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']