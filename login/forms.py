from django import forms
from login.models import Post,User_details, Comments
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from django.contrib.auth.models import User


class Post_form(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3', 'style':' box-shadow: 0 1px 2px 0 lightblue, 0 2px 10px 0 lightblue;'}))

    class Meta:
        model = Post
        fields = {'text'}


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


class Edit_profile(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'firstname'}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lastname'}))


class CommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                        'style': ' box-shadow: 0 1px 2px 0 lightblue, 0 2px 10px 0 lightblue;'}))

    class Meta:
        model = Comments
        fields = {'text'}


class Personal_details(ModelForm):
    interests = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg: c,python,c++,java'}))

    class Meta:
        model = User_details
        fields = {'phone','image','date_of_birth','interests'}
        date_of_birth = forms.DateField(
            widget=forms.DateInput(format='%m/%d/%Y'),
            input_formats=('%m/%d/%Y',)
        )
        phone = forms.RegexField(regex=r'^\d{9,15}$')
