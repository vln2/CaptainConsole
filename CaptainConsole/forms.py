from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order, Item


class OrderForms(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreatingUserForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-10'}),
            'email': forms.EmailInput(attrs={'class': 'form-control col-sm-10'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control col-sm-10'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control col-sm-10'})
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-10'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control col-sm-10'})
        }

class AddItemToCartForm(ModelForm):
    class Meta:
        model = Item
        fields = ('quantity',)
