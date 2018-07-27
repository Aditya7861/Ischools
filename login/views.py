from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.forms import Login


def home(request):
    return render(request, 'home.html')


def login(request):
    form = Login()
    return render(request, 'login.html',{'form':form})


def loggedin(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            return render(request, 'loggedin.html', {'user':username})
        else:
            return HttpResponse("not valid")
