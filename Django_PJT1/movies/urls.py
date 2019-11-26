from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search_movie/', views.search_movie, name='search_movie'),
    path('<int:movie_id>/like/', views.toggle_like, name='like'),
]
