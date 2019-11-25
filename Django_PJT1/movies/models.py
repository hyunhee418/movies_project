from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    MovieCd = models.IntegerField()
    movieName = models.CharField(max_length=30)
    movieNameE = models.CharField(max_length=30)
    pubDate = models.IntegerField()
    runtime = models.CharField(max_length=200)
    # genre = models.IntegerField()
    director = models.CharField(max_length=200)
    userRating = models.FloatField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()

class Movie_has_genre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
# class Movie(models.Model):
#     title = models.CharField(max_length=30)
#     audience = models.IntegerField()
#     poster_url = models.CharField(max_length=140)
#     description = models.TextField()
#     movie_genres = models.ManyToManyField(Genre, related_name='genre_movies')
#     like_users = models.ManyToManyField(User, related_name='like_movies')
    
# class Review(models.Model):
#     content = models.CharField(max_length=140)
#     score = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)