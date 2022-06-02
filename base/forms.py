from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['profile_picture']