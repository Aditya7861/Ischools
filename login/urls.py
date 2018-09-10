from django.urls import path
from login import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('loggedin/(?P<pk>\d+)/following/',views.followers, name='followers'),
    path('post/',views.user_post, name='userpost'),
    path('friends/',views.friends, name='friends'),
    path('loggedin/(?P<pk>\d+)/profile/', views.profile, name='profile'),
    path('update_user/', views.update_user, name='update_user'),
    path('post/(?P<pk>\d+)/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/(?P<pk>\d+)/post_deatil/', views.post_details,name='post_details'),
    path('post/(?P<pk>\d+)/likes', views.add_like,name= 'add_like'),
    path('post/(?P<pk>\d+)/unlike', views.delete_like, name= 'delete_like'),
    path('friends/(?P<pk>\d+)/follow', views.follow,name='follow'),
    path('friends/(?P<pk>\d+)/unfollow', views.unfollow, name='unfollow'),
    path('profile/(?P<pk>\d+)/my_posts/', views.my_posts, name='my_posts'),
    path('profile/myposts/(?P<pk>\d+)/delete_post', views.delete_post, name='delete_post'),
]
