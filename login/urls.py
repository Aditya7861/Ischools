from django.urls import path
from login import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('loggedin/', views.loggedin, name='loggedin'),
]