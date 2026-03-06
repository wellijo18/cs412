# mini_insta/models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  '''encapsulate the data of a blog article by an author'''
  user = models.ForeignKey(User, on_delete=models.CASCADE)
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
  
  def get_absolute_url(self):
    '''return to the profile'''
    return f"/mini_insta/profile/{self.pk}"
  def get_followers(self):
    '''return a list of profiles that follow this profile'''
    follows = Follow.objects.filter(profile=self)
    followers = []
    for follow in follows:
        followers.append(follow.follower_profile)
    return followers
  def get_num_followers(self):
      '''return the number of followers this profile has'''
      return len(self.get_followers())

  def get_following(self):
    '''return a list of profiles that this profile follows'''
    follows = Follow.objects.filter(follower_profile=self)
    following = []
    for follow in follows:
        following.append(follow.profile)
    return following

  def get_num_following(self):
      '''return the number of profiles this profile is following'''
      return len(self.get_following())
  def get_num_posts(self):
    '''return the number of posts this profile has'''
    return len(self.get_all_posts())
  def get_post_feed(self):
    '''return the list of posts from profiles that profile follows'''
    following = self.get_following()
    posts = []
    for profile in following:
        profile_posts = profile.get_all_posts()
        for post in profile_posts:
            posts.append(post)
    posts = sorted(posts, key=lambda post: post.timestamp, reverse=True)
    return posts

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
  def get_all_comments(self):
    '''return a QuerySet of comments on this post'''
    comments = Comment.objects.filter(post=self).order_by('-timestamp')
    return comments

  def get_likes(self):
    '''return likes on this post'''
    likes = Like.objects.filter(post=self)
    return likes

class Photo(models.Model):
  '''Encapsulate the Photo attached to comment'''

  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image_url = models.URLField(blank=True)
  image_file= models.ImageField(blank=True)
  timestamp=models.DateTimeField(auto_now=True)

  def __str__(self):
    '''return a string representation of this Post'''
    if self.image_url:
      return f'{self.image_url} attached to post'
    elif self.image_file:
      return f'{self.image_file.url} attached to post'
    else:
      return "No image attached"
  
  def get_image_url(self):
    '''for grabbing umage url for database'''
    if self.image_url:
      return self.image_url
    elif self.image_file:
      return self.image_file.url
    return ""

class Follow(models.Model):
  '''Encapsulate the follow between two profiles'''
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
  follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
  timestamp = models.DateTimeField(auto_now=True)

  def __str__(self):
    '''return a string representation of Follow'''
    return f'{self.follower_profile.username} follows {self.profile.username}'

class Comment(models.Model):
  '''Encapsulate the comment of a post'''

  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)
  text = models.TextField(blank=False)
  def __str__(self):
    '''return a string representation of Comment'''
    return f'{self.profile.username} commented on {self.post.caption}'

class Like(models.Model):
  '''Encapsulate like on a post'''
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)

  def __str__(self):
    '''return a string representation of Like'''
    return f'{self.profile.username} liked {self.post.caption}'
