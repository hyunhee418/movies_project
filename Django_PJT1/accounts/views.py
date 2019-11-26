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
    return render(request, 'accounts/user_page.html', {
        'user_info' :user,
    })

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

def checked(request):
    if request.method == "POST":
        checked_list = request.POST.get('checked_data')
        print('--------------------')
        print(checked_list)
        return redirect('movies:movie_list')