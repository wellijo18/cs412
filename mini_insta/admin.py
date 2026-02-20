#mini_isnta/admin.py
from django.contrib import admin

# Register your models here.
from .models import Profile, Photo, Post
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Post)