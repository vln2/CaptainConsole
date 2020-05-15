from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order, Item, Address, Payment

# bootstrap class styles for input forms
sInputClass = "form-control col-sm-12 col-md-8 col-lg-6"

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class OrderForms(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
  

class CreatingUserForms(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = sInputClass
        self.fields['password2'].widget.attrs['class'] = sInputClass
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': sInputClass}),
            'email': forms.EmailInput(attrs={'class': sInputClass}),
            'password1': forms.PasswordInput(attrs={'class': sInputClass}),
            'password2': forms.PasswordInput(attrs={'class': sInputClass})
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = sInputClass
        self.fields['password'].widget.attrs['class'] = sInputClass

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class AddItemToCartForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['class'] = "form-control"
        self.fields['quantity'].widget.attrs['min'] = 1
    class Meta:
        model = Item
        fields = ('quantity',)


class RemoveItemFromCartForm(ModelForm):
    class Meta:
        model = Item
        fields = ('quantity',)


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'street': forms.TextInput(attrs={'class': "form-control"}),
            'postalCode': forms.TextInput(attrs={'class': "form-control"}),
            'city': forms.TextInput(attrs={'class': "form-control"}),
            'country': forms.TextInput(attrs={'class': "form-control"})
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'cardNumber': forms.TextInput(attrs={'class': "form-control"}),
            'cardName': forms.TextInput(attrs={'class': "form-control"}),
            'cardExp': forms.TextInput(attrs={'class': "form-control"}),
            'status': forms.TextInput(attrs={'class': "form-control"}),
            'cardCVC': forms.TextInput(attrs={'class': "form-control"})
        }

