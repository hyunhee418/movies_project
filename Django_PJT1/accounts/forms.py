from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from accounts.models import Image, Damgle
User = get_user_model()

from django import forms
# from .models import Damgle


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'introduction',)

class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = User

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file', )
        widgets = {
            'file': forms.FileInput(attrs={'multiple': True})
        }

class DamgleForm(forms.ModelForm):
    class Meta:
        model = Damgle
        fields = ('content',)