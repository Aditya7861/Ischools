from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from login.forms import Login,SignUpForm,Post_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from login.models import Post
from django.utils import timezone


def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/loggedin/')
            else:
                return HttpResponse("user not found.")
    else:
        form = Login()
    return render(request, 'login.html', {'form': form})


@login_required()
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required()
def user_post(request):
    if request.method == 'POST':
        postform = Post_form(request.POST)
        if postform.is_valid():
            obj = postform.save(commit=False)
            obj.username = request.user
            obj.published_date = timezone.now()
            obj.save()
            return redirect('loggedin')
    return redirect('loggedin')


@login_required()
def loggedin(request):
    form = Post_form
    post = Post.objects.all()
    return render(request, 'loggedin.html', {'form':form,'posts':post})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/loggedin/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
