from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'introduction',)

class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = User