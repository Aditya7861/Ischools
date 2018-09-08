from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.username


class User_details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone = models.IntegerField()
    image = models.ImageField(upload_to='profile_image', blank=True)


class Comments(models.Model):
    post = models.ForeignKey('Post', on_delete= models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField()

    def __str__(self):
        return self.text


class Likes(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    liked_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user}"
