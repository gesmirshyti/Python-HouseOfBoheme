from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
    # first_name = forms.CharField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username',  'password1' ,'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True , label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


class CheckoutForm(AuthenticationForm):
    first_name = forms.CharField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(required=True , widget=forms.TextInput(attrs={'class':'form-control'}))
    card_number = forms.IntegerField(required=True , widget=forms.NumberInput(attrs={'class':'form-control'}))
    cvv_number = forms.IntegerField(required=True , widget=forms.NumberInput(attrs={'class':'form-control'}))
    zip_code  = forms.IntegerField(required=True , widget=forms.NumberInput(attrs={'class':'form-control'}))

