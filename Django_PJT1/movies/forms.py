from django import forms
from .models import Movie, Genre, Review

class ReviewForm(forms.ModelForm):
    content = forms.CharField(max_length=500)
    score = forms.IntegerField(max_value=5, min_value=1)
    class Meta:
        model = Review
        fields = ('content', 'score', )