from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Login(forms.Form):
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'firstname'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'lastname'}))
    email = forms.EmailField(max_length=254,)
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        help_texts={'password1':'enter'}
