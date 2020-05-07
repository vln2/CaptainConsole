from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.model import User
from django import forms

from .models import Order

class OrderForms(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreatingUserForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'passwordI', 'passwordII', 'address']