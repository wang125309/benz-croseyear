from django.db import models

# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length = 255)
    like1 = models.IntegerField()
    like2 = models.IntegerField()
    tickets1 = models.IntegerField()
    tickets2 = models.IntegerField()
    src = models.CharField(max_length = 255)

class Like(models.Model):
    userid = models.IntegerField()
    toUserid = models.IntegerField()
    type = models.IntegerField()
