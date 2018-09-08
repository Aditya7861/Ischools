from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from login.forms import Login,SignUpForm,Post_form,Edit_profile,Personal_details,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from login.models import Post,User_details,Likes
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
def add_like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    liked_date = timezone.now()
    l = Likes(post=post,user=user,liked_date=liked_date)
    l.save()
    return redirect('loggedin')


@login_required()
def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    return render(request, 'post_details.html',{'post':post,'form':form})


@login_required()
def add_comment_to_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            cobj = commentform.save(commit=False)
            cobj.post = post
            cobj.created_date = timezone.now()
            cobj.author = request.user
            cobj.save()
            return redirect('post_details', pk=post.pk)
    return redirect('post_details', pk=post.pk)


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
def profile(request):
    users = User.objects.all()
    return render(request, 'profile.html', {'users': users})


@login_required()
def friends(request):
    users = User.objects.all()
    return render(request, 'friends.html', {'users':users})


@login_required()
def loggedin(request):
    form = Post_form

    post = Post.objects.all().order_by('-published_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(post,4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'loggedin.html', {'form': form, 'posts': users,})


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


@login_required
def update_user(request):
    if request.method == "POST":
        update_user_form = Edit_profile(request.POST, instance=request.user)
        update_profile_form = Personal_details(request.POST, request.FILES, instance= User_details)

        if update_user_form.is_valid() and update_profile_form.is_valid():
            user = update_user_form.save()
            profile = update_profile_form.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            return redirect('updateuser')
    else:
        update_user_form = Edit_profile(instance= request.user)
        update_profile_form = Personal_details(instance= User_details)

    return render(request,'edit_profile.html',{'form1':update_user_form, 'form2':update_profile_form})