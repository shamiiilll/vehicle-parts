from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description")



class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    part = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.part