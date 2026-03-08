from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description")

class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  


