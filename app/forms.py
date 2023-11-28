from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASSES
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': INPUT_CLASSES
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': INPUT_CLASSES
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': INPUT_CLASSES
    }))