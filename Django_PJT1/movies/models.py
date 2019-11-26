from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
# User = get_user_model()
User = settings.AUTH_USER_MODEL

class Genre(models.Model):
    name = models.CharField(max_length=20)
class Movie(models.Model):
    MovieCd = models.IntegerField()
    movieName = models.CharField(max_length=30)
    movieNameE = models.CharField(max_length=30)
    pubDate = models.IntegerField()
    runtime = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie_genre') # 여기가 변경사항
    director = models.CharField(max_length=200)
    userRating = models.FloatField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    like_users = models.ManyToManyField(User, related_name='like_movies')
    
class Review(models.Model):
    content = models.CharField(max_length=150)
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)