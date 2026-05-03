from django.contrib.auth.models import User
from hostel.models import Room, Student, Fee, Complaint

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hostel.com', 'admin')

if not Room.objects.exists():
    Room.objects.create(room_no='101', room_type='Single', capacity=1)
    Room.objects.create(room_no='102', room_type='Double', capacity=2)
    Room.objects.create(room_no='103', room_type='Triple', capacity=3)

if not Student.objects.exists():
    Student.objects.create(name='John Doe', email='john@student.com', phone='1234567890')
