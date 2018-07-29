from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from login.forms import Login,SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout


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
def loggedin(request):
    user = request.user
    return render(request, 'loggedin.html', {'user':user})


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
