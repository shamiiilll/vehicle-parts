from django.db import models
from users.models import User

class Complaint(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, default='pending')