from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('checked/', views.checked, name='checked'),
    path('user_page/<int:user_id>/', views.user_page, name='user_page'),
]