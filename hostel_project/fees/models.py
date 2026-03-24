from django.db import models
from users.models import User

class Fee(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending')
    ])