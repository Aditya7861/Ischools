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
]
