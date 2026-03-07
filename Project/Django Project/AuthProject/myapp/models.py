from django.db import models

# Create your models here.

class usersignup(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.BigIntegerField(max_length=10)
    city = models.CharField(max_length=20)
    password = models.CharField(max_length=20)