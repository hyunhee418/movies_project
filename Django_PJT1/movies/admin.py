from django.contrib import admin
from .models import Movie

class MovieModelAdmin(admin.ModelAdmin):
    list_display = 'id', 'MovieCd', 'movieName', 'movieNameE', 'pubDate', 'runtime', 'director', 'userRating', 'poster_url', 'description', 'genre'

admin.site.register(Movie, MovieModelAdmin)