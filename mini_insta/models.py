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

  def get_all_posts(self):
    '''return a QuerySet of posts made on a profile'''
    posts = Post.objects.filter(profile=self).order_by('-timestamp')
    return posts

  def __str__(self):
    '''return a string representation of this model'''
    return f'{self.display_name} account created by {self.username}'

class Post(models.Model):
  '''Encapsulate the idea of a comment about an Post'''

  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  caption = models.TextField(blank=False)
  timestamp=models.DateTimeField(auto_now=True)

  def __str__(self):
    '''return a string representation of this Post'''
    return f'{self.caption} made at {self.timestamp}'

  def get_all_photos(self):
    '''return a QuerySet of comments about this article'''
    photos = Photo.objects.filter(post=self).order_by('-timestamp')
    return photos

class Photo(models.Model):
  '''Encapsulate the idea of a comment about an Photo'''

  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image_url = models.URLField(blank=True)
  timestamp=models.DateTimeField(auto_now=True)

  def __str__(self):
    '''return a string representation of this Post'''
    return f'{self.image_url} attached to post'
