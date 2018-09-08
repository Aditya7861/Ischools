from django import forms
from phone_field import  PhoneFormField
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


class Edit_profile(UserChangeForm):

    def __init__(self, *args, **kargs):
        super(Edit_profile, self).__init__(*args, **kargs)
        del self.fields['password']
        self.clean()

    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email'}
        exclude = {'password'}


class CommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                        'style': ' box-shadow: 0 1px 2px 0 lightblue, 0 2px 10px 0 lightblue;'}))
    class Meta:
        model = Comments
        fields = {'text'}


class Personal_details(ModelForm):
    YEARS = [x for x in range(1980, 2050)]
    phone = forms.IntegerField()
    image = forms.ImageField()
    dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = User_details
        fields = {'phone', 'image'}

