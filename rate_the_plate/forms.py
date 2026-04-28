from django import forms
from .models import Review, Comment

class CreateReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(0, 11)]
    )

    class Meta:
        model = Review
        fields = ['rating', 'review_text']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']