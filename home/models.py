from django.db import models

# Create your models here.

class OurTeam(models.Model):
    name=models.CharField(max_length=100)
    post=models.TextField()
    img=models.ImageField(upload_to='pics')
    fb=models.TextField()
    tw=models.TextField()
    link=models.TextField()
    insta=models.TextField()

class Contect_admin(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.CharField(max_length=300)
