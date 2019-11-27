from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomAuthenticationForm, CustomUserCreationForm, DamgleForm
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from movies.models import Movie, Genre
from django.db.models import Max
from accounts.models import Damgle
User = get_user_model()

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return render(request, 'movies/movie_list.html')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            movies = Movie.objects.all()[50:141]
            return render(request, 'accounts/choice.html', {
                'movies':movies
            })

    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/user_form.html', {
        'form':form
    })

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:movie_list')

    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/user_form.html', {
        'form':form,
    })

def logout(request):
    auth_logout(request)
    return redirect('movies:movie_list')


@require_http_methods(['GET'])
def user_page(request, user_id):
    user = get_object_or_404(User, id = user_id)
    damgle_form = DamgleForm()
    damgles = Damgle.objects.filter(page_master_id = user_id).exists()
    return render(request, 'accounts/user_page.html', {
        'user_info' : user,
        'damgle_form' : damgle_form,
        'damgles' : damgles,
    })
    # return render(request, 'accounts/user_page.html', {
    #     'user_info' : user,
    #     
    # })

@require_http_methods(['GET', 'POST'])
def edit_user_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        # form = ArticleModelForm(request.POST) 이렇게 쓰면 새종이에 데이터 쓰는 것이고 instance=article 하면 있는 데이터에 덮어써서 수정하는 것
        form = CustomUserCreationForm(request.POST, instance=user) # 사용자가 '새로 입력한 데이터'를 미리 만들어둔 case에 넣음
        if form.is_valid():
            user = form.save()
            return redirect('movies:user_page', user_id)
    # 사용자가 수정하기 위한 html 파일을 요청함/ 있던 데이터를 찾아서 html에 넣어서 보내줌
    else:        
        form = CustomUserCreationForm(instance=user)
    # 위와 겹치므로 한칸 앞으로 가서 코드 간단히 해줌
    return render(request, 'accounts/user_form.html', {
        'form':form,
    })
    

def test(request):
    movies = Movie.objects.all()[50:141]
    return render(request, 'accounts/choice.html', {
        'movies':movies
    })

@login_required
def checked(request):
    if request.method == "POST":
        # 어떤 장르 영화를 좋아하는 지
        genre = [0]*28
        checked_list = request.POST.getlist('checked_data')
        user = request.user
        for i in checked_list:
            genre_id, movie_id = i.split(',')
            genre[int(genre_id)] += 1
            movie = get_object_or_404(Movie, id = int(movie_id))
            user.like_movies.add(movie)
        max_point1, max_idd1, max_point2, max_idd2 = 0, 0, 0, 0
        for j in range(28):
            if max_point1 < genre[j]:
                max_point1 = genre[j]
                max_idd1 = j
            else:
                if max_point2 < genre[j]:
                    max_point2 = genre[j]
                    max_idd2 = j
        genre1 = get_object_or_404(Genre, id=max_idd1)
        genre2 = get_object_or_404(Genre, id=max_idd2)
        user.like_genres.add(genre1)
        user.like_genres.add(genre2)
        # 추천 알고리즘
        movie = Movie.objects.filter(genre_id=genre1).order_by('-userRating').distinct()[:1]
        movies1 = Movie.objects.filter(genre_id=genre1).order_by('-userRating').distinct()[1:11]
        movies2 = Movie.objects.filter(genre_id=genre2).order_by('-userRating').distinct()[:10]
        # 취향 비슷한 사람 찾기
        users = []
        for user in User.objects.all():
            genre_li = []
            for like_genre in user.like_genres.all():
                genre_li.append(like_genre.id)
            if sorted(genre_li) == sorted([max_idd1, max_idd2]):
                users.append(user)
        return render(request, 'movies/movie_list.html', {
            'movie': movie,
            'movies1' : movies1,
            'movies2' : movies2,
            'users': users,
        })

@login_required
@require_POST
def create_damgle(request, page_master_id):
    page_master = get_object_or_404(User, id=page_master_id)
    if request.method == 'POST':
        damgle_form = DamgleForm(request.POST)
        if damgle_form.is_valid():
            damgle = damgle_form.save(commit=False)
            damgle.user = request.user
            damgle.page_master = page_master
            damgle.save()
        return redirect('accounts/user_page.html', page_master.id)