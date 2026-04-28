# rate_the_plate/forms.py
from django import forms
from .models import Review, Comment

class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']