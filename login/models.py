from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.username


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")


