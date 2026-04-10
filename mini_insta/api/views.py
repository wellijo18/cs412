# mini_insta/api/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from ..models import Profile, Post
from .serializers import MIProfileSerializer, MIPostSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def LoginAPIView(request):
    '''login da user'''
    username = request.data.get('username')

    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user == None:
        return Response({'error': 'Invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    profile = Profile.objects.get(user=user)
    data = {
        'token': token.key,
        'profile_id': profile.pk
    }
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfileListAPIView(request):
    '''get all da profiles'''
    profiles = Profile.objects.all()
    serializer = MIProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfileDetailAPIView(request, pk):
    '''get one profile'''
    profile = Profile.objects.get(pk=pk)
    serializer = MIProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfilePostsAPIView(request, pk):
    '''get da posts for one profile'''
    profile = Profile.objects.get(pk=pk)
    posts = profile.get_all_posts()
    serializer = MIPostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfileFeedAPIView(request, pk):
    '''get da feed posts'''
    profile = Profile.objects.get(pk=pk)
    feed_posts = profile.get_post_feed()
    serializer = MIPostSerializer(feed_posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def CreatePostAPIView(request, pk):
    '''make a new post'''
    profile = Profile.objects.get(pk=pk)

    serializer = MIPostSerializer(data=request.data)

    if serializer.is_valid():
        post = serializer.save(profile=profile)
        return Response(MIPostSerializer(post).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)