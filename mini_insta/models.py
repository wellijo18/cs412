# mini_insta/models.py
from django.db import models

# Create your models here.
class Profile(models.Model):
  '''encapsulate the data of a blog article by an author'''
  username=models.TextField(blank=True)
  display_name=models.TextField(blank=True)
  profile_image_url = models.URLField(blank=True)
  bio_text=models.TextField(blank=True)
  join_date=models.DateTimeField(auto_now=True)
  # user_followers=models.IntegerField(blank=True)
  # user_follows=models.IntegerField(blank=True)

  def __str__(self):
    '''return a string representation of this model'''
    return f'{self.display_name} account created by {self.username}'
