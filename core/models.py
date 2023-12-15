from django.db import models

# Create your models here.
class History(models.Model):
    text = models.TextField(max_length=500)

class Result(models.Model):
    word = models.CharField(max_length=500,blank=True)
    label_group = models.CharField(max_length=500,blank=True)
