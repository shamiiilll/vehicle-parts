from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User

from rooms.models import Room
from fees.models import Fee
from complaints.models import Complaint
from notices.models import Notice


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        if request.POST['password'] != request.POST['confirm_password']:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            role=request.POST['role']
        )
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    rooms = Room.objects.all()
    fees = Fee.objects.all()
    complaints = Complaint.objects.all()
    notices = Notice.objects.all()
    students = User.objects.filter(role='student')

    return render(request, 'dashboard.html', {
        'rooms': rooms,
        'fees': fees,
        'complaints': complaints,
        'notices': notices,
        'students': students,

        'chart_data': [
            rooms.count(),
            fees.count(),
            complaints.count(),
            notices.count()
        ]
    })


@login_required
def rooms(request):
    if request.method == "POST":
        Room.objects.create(
            room_number=request.POST['room_number'],
            capacity=request.POST['capacity']
        )
    return render(request, 'rooms.html', {'rooms': Room.objects.all()})


@login_required
def fees(request):
    return render(request, 'fees.html', {'fees': Fee.objects.all()})


@login_required
def complaints(request):
    if request.method == "POST":
        Complaint.objects.create(
            student=request.user,
            message=request.POST['message']
        )
    return render(request, 'complaints.html', {
        'complaints': Complaint.objects.all()
    })


@login_required
def notices(request):
    if request.method == "POST":
        Notice.objects.create(
            title=request.POST['title'],
            content=request.POST['content']
        )
    return render(request, 'notices.html', {
        'notices': Notice.objects.all()
    })

@login_required
def students(request):
    from .models import User
    return render(request, 'students.html', {
        'students': User.objects.filter(role='student')
    })