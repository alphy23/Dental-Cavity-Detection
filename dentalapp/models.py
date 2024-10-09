from django.db import models

# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=30)
    uname=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=30)
    cpassword=models.CharField(max_length=30)
    age=models.IntegerField()
    gender=models.CharField(max_length=30)

class normal(models.Model):
    img = models.ImageField(upload_to='normalteeth/')

class xray(models.Model):
    ximg = models.ImageField(upload_to='xrayteeth/')    