from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=127)
    mobile = models.CharField(max_length=127)
    avatar = models.CharField(max_length=512)
    desc = models.TextField()
    like = models.IntegerField()
    dateline = models.CharField(max_length=127)
