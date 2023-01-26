from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import product
from django.utils.translation import gettext_lazy as _

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        label="姓名",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="手機",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="電話",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )