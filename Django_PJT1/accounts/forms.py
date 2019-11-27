from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

from django import forms
from .models import Damgle


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'introduction',)

class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = User

class DamgleForm(forms.ModelForm):
    class Meta:
        model = Damgle
        fields = ('content',)