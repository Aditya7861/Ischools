from django.db import models
# Create your models here.


class Post(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.username

