# ratemyplate/admin.py

from django.contrib import admin

# Register your models here.
from .models import Car, Review, ReviewReaction, Comment

admin.site.register(Car)
admin.site.register(Review)
admin.site.register(ReviewReaction)
admin.site.register(Comment)