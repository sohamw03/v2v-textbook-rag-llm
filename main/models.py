from django.db import models


# Create your models here.
class Chat(models.Model):
    author = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    name = models.CharField(max_length=200)
    mode = models.CharField(max_length=200)
