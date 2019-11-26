from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Movie, Genre
User = get_user_model()


# Create your views here.
def movie_list(request):
    user = request.user
    genres = user.like_genres.all()
    li = []
    users = []
    for genre in genres:
        li.append(genre.id)
    movies1 = Movie.objects.filter(genre_id=li[0]).order_by('-userRating').distinct()[:10]
    movies2 = Movie.objects.filter(genre_id=li[1]).order_by('-userRating').distinct()[:10]

    for user in User.objects.all():
        genre_li = []
        for like_genre in user.like_genres.all():
            genre_li.append(like_genre.id)
        if sorted(genre_li) == sorted(li):
            users.append(user)
    if not users:
        users = User.objects.all()
    return render(request, 'movies/movie_list.html', {
        'movies1' : movies1,
        'movies2' : movies2,
        'users':users
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    genre = get_object_or_404(Genre, id=movie.genre_id)
    is_like = movie.like_users.filter(id=request.user.id).exists()
    # review_form = ReviewForm()
    # is_like = movie.like_users.filter(id=request.user.id).exists()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'genre': genre,
        # 'review_form': review_form,
        'is_like': is_like,
    })
    
def search_movie(request):
    search_movie = request.GET.get('search_movie')
    print(search_movie)
    search_movies = Movie.objects.filter(movieName__contains=search_movie).distinct()
    print(search_movies)
    return render(request, 'movies/search_movie.html', {'search_movies': search_movies})
        

@require_POST
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    # 좋아요를 누른 유저라면
    if movie.like_users.filter(id=user.id).exists():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
    genre = [0]*28
    for user_movie in user.like_movies.all():
        genre[user_movie.genre_id] += 1
    max_point1, max_idd1, max_point2, max_idd2 = 0, 0, 0, 0
    for j in range(28):
        if max_point1 < genre[j]:
            max_point1 = genre[j]
            max_idd1 = j
        else:
            if max_point2 < genre[j]:
                max_point2 = genre[j]
                max_idd2 = j
    for i in user.like_genres.all():
        user.like_genres.remove(i)
    genre1 = get_object_or_404(Genre, id=max_idd1)
    genre2 = get_object_or_404(Genre, id=max_idd2)
    user.like_genres.add(genre1)
    user.like_genres.add(genre2)
    return redirect('movies:movie_detail', movie.id)
