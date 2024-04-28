from django.db import models
from django.shortcuts import reverse

class Category(models.Model):
  name=models.CharField(max_length=100,unique=True)

  def __str__(self):
    return self.name
  