from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Movie, Genre

# Create your views here.
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    for movie_genre in movie.movie_genre.all():
        genre = get_object_or_404(Genre, id=movie_genre.genre.id)
        break
    # review_form = ReviewForm()
    # is_like = movie.like_users.filter(id=request.user.id).exists()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'genre': genre,
        # 'review_form': review_form,
        # 'is_like': is_like,
    })
