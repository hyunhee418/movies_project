from django.contrib import admin

# Register your models here.
from .models import Movie, Genre, Movie_has_genre

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Movie_has_genre)