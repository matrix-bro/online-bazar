from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django_recaptcha.fields import ReCaptchaField
from app.models import ConversationMessage, Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

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
    captcha = ReCaptchaField(error_messages={'required': 'Please complete the captcha.'})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASSES
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': INPUT_CLASSES
    }))
    captcha = ReCaptchaField(error_messages={'required': 'Please complete the captcha.'})

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)  

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Product Name',
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description',
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'placeholder': 'Price',
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }  

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold',)  

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }          

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            })
        }
            