from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)

    def is_available(self):
        return self.occupied < self.capacity