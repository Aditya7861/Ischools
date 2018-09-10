from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from login.forms import Login,SignUpForm,Post_form,Edit_profile,Personal_details,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from login.models import Post,User_details,Likes,Following
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
def my_posts(request,pk):
    user = User.objects.get(pk=pk)
    posts = user.post_set.all().order_by('-published_date')
    return render(request,'my_posts.html',{'posts':posts})


@login_required()
def delete_post(request,pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('my_posts')


@login_required()
def add_like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    liked_date = timezone.now()
    l = Likes(post=post, user=user, liked_date=liked_date)
    l.save()
    return redirect('loggedin')


@login_required()
def delete_like(request, pk):
    post = Post.objects.get(pk=pk)
    like = Likes.objects.get(post=post, user=request.user)
    like.delete()
    return redirect('loggedin')


@login_required()
def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    return render(request, 'post_details.html',{'post': post, 'form':form})


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
def profile(request,pk):
    user = User.objects.get(pk=pk)
    return render(request, 'profile.html', {'user': user})


@login_required()
def friends(request):
    users = User.objects.all().exclude(pk=request.user.id)
    li2 = []
    fols = Following.objects.filter(user_id=request.user.id)
    for fol in fols:
        li2.append(fol.friend.username)
    return render(request, 'friends.html', {'users':users,'followers':fols,'followlist':li2})


@login_required()
def followers(request,pk):
    user = User.objects.get(pk=pk)
    return render(request,'following.html',{'user':user})


@login_required()
def follow(request, pk):
    friend = User.objects.get(pk=pk)
    user = request.user
    f = Following(user=user, friend=friend)
    f.save()
    return redirect('friends')


@login_required()
def unfollow(request, pk):
    user1 = User.objects.get(pk=pk)
    user = User.objects.get(pk=request.user.id)
    follower = user.following_set.get(friend_id=user1.id)
    follower.delete()
    return redirect('friends')


@login_required()
def loggedin(request):
    form = Post_form
    likes = Likes.objects.filter(user_id=request.user.id)
    li = []
    for like in likes:
        li.append(like.post_id)
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.filter(username__following__friend_id=user.id).order_by('-published_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'loggedin.html', {'form': form, 'posts': post,'likes':li})


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
    if request.method == 'POST':
        form1 = Edit_profile(request.POST)
        form2 = Personal_details(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = User.objects.get(username=request.user)
            user.first_name = form1.cleaned_data.get('first_name')
            user.last_name = form1.cleaned_data.get('last_name')
            user.save()
            if User_details.objects.filter(user=request.user).exists() :
                user = User_details.objects.get(user=request.user)
                user.date_of_birth = form2.cleaned_data.get('date_of_birth')
                user.image = form2.cleaned_data.get('image')
                user.phone = form2.cleaned_data.get('phone')
                user.interests = form2.cleaned_data.get('interests')
                user.save()
                print("success")
            else:
                print("not-success")
                user = request.user
                phone = form2.cleaned_data.get('phone')
                image = form2.cleaned_data.get('image')
                dob = form2.cleaned_data.get('date_of_birth')
                f = User_details(user=user,phone=phone,image=image,date_of_birth=dob)
                f.save()
            return redirect('profile',pk=request.user.id)
    else:
        form1 = Edit_profile()
        form2 = Personal_details()
    return render(request,'edit_profile.html',{'form1':form1, 'form2':form2})