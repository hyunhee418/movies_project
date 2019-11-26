from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from movies.models import Movie
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
    return render(request, 'accounts/signup.html', {
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
    return render(request, 'accounts/login.html', {
        'form':form,
    })

def logout(request):
    auth_login(request)
    return redirect('movies:movie_list')


@require_http_methods(['GET'])
def user_page(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return render(request, 'accounts/user_page.html', {
        'user_info' :user,
    })

def test(request):
    movies = Movie.objects.all()[50:141]
    return render(request, 'accounts/choice.html', {
        'movies':movies
    })

def checked(request):
    if request.method == "POST":
        checked_list = request.POST.get('checked_data')
        print('--------------------')
        print(checked_list)
        return redirect('movies:movie_list')