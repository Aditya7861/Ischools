from django.urls import path
from login import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('post/',views.user_post, name='userpost'),
    path('friends/',views.friends, name='friends'),
    path('profile/', views.profile, name='profile'),
    path('update_user/',views.update_user, name='updateuser'),
    path('post/(?P<pk>\d+)/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/(?P<pk>\d+)/post_deatil/',views.post_details,name='post_details'),
    path('post/(?P<pk>\d+)/likes', views.add_like,name= 'add_like'),
]
