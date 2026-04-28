from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Car(models.Model):
    state = models.CharField(max_length=15, blank=False)
    license_plate = models.CharField(max_length=8, blank=False)
    make = models.CharField(max_length=15, blank=True)
    model = models.CharField(max_length=15, blank=True)
    color = models.CharField(max_length=10, blank=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.license_plate} ({self.state})'

    def get_absolute_url(self):
        return reverse('car', kwargs={'pk': self.pk})


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    review_text = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.car} by {self.user.username}'

    def get_absolute_url(self):
        return reverse('review', kwargs={'pk': self.pk})


class ReviewReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.reaction}d {self.review.user.username}\'s review'

    def get_absolute_url(self):
        return reverse('reaction', kwargs={'pk': self.pk})


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.review}'

    def get_absolute_url(self):
        return reverse('comment', kwargs={'pk': self.pk})