from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search_movie/', views.search_movie, name='search_movie'),
    path('<int:movie_id>/like/', views.toggle_like, name='like'),
    path('<int:movie_id>/reviews/create/', views.create_review, name='create_review'),
    # path('<int:movie_id>/reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:movie_id>/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
