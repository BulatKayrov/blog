from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'image')
