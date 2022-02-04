from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

class Post(models.Model):
    post_time = models.DateField(auto_now=True)
    title = models.CharField(max_length=200)
    text = models.TextField()