import json
import csv
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Student, Room, Fee, Complaint, Attendance, Notice
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.contrib import messages

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:
          messages.error(request, "Invalid role selected")

    return render(request, "login.html")



def register_page(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Email already undo check
        if User.objects.filter(username=email).exists():

            messages.error(request, "Email already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        if role == "admin":
            user.is_superuser = True
            user.is_staff = True
            user.save()

        messages.success(request, "Registration successful")

        return redirect("login")

    return render(request, "register.html")
def rooms_page(request):
    return render(request, 'rooms.html')


def students_page(request):
    return render(request, 'students.html')


def fees_page(request):
    return render(request, 'fees.html')


def complaints_page(request):
    return render(request, 'complaints.html')

def dashboard_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    students_count = Student.objects.count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(
        occupied__lt=F('capacity')
    ).count()

    totals = Room.objects.aggregate(
        total_capacity=Sum('capacity'),
        total_occupied=Sum('occupied')
    )

    tc = totals['total_capacity'] or 1
    to = totals['total_occupied'] or 0

    occupancy_rate = (to / tc) * 100 if tc > 0 else 0

    pending_fees = Fee.objects.filter(
        status__in=['Pending', 'Overdue']
    ).count()

    pending_complaints = Complaint.objects.filter(
        status='Pending'
    ).count()

    context = {
        'is_admin': request.user.is_superuser,
        'user_name': request.user.username,
        'students_count': students_count,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupancy_rate': occupancy_rate,
        'pending_fees': pending_fees,
        'pending_complaints': pending_complaints,
    }

    return render(request, 'dashboard.html', context)
def logout_page(request):

    logout(request)

    return redirect('login')



    

def api_data(request):
    rooms = list(Room.objects.values('room_no', 'room_type', 'capacity', 'occupied', 'status'))
    students = list(Student.objects.annotate(room_no=F('room__room_no')).values('id', 'name', 'email', 'phone', 'room_no'))
    complaints = list(Complaint.objects.annotate(student_name=F('student__name')).values('id', 'student_name', 'category', 'description', 'status'))
    fees = list(Fee.objects.annotate(student_name=F('student__name')).values('id', 'student_name', 'amount', 'month', 'status', 'date_paid'))
    
    today = timezone.now().date()
    attendance = list(Attendance.objects.filter(date=today).annotate(student_name=F('student__name')).values('id', 'student_name', 'status', 'date'))
    notices = list(Notice.objects.values('id', 'title', 'content', 'date_posted').order_by('-date_posted'))
    return JsonResponse({'rooms': rooms, 'students': students, 'complaints': complaints, 'fees': fees, 'attendance': attendance, 'notices': notices})

@csrf_exempt
def add_student(request):

    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")

    if request.method == 'POST':
        data = json.loads(request.body)
        Student.objects.create(name=data['name'], email=data['email'], phone=data['phone'])
        return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_student(request, id):

    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")

    if request.method == 'POST':
        st = Student.objects.get(id=id)
        if st.room:
            st.room.occupied -= 1
            st.room.save()
        st.delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def add_room(request):

    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        capacity = 1 if data['type'] == 'Single' else (2 if data['type'] == 'Double' else 3)
        Room.objects.create(room_no=data['no'], room_type=data['type'], capacity=capacity)
        return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_room(request, no):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    if request.method == 'POST':
        Room.objects.filter(room_no=no).delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def allocate_room(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Admins only")

    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            student = Student.objects.get(id=data['student_id'])
            room = Room.objects.get(room_no=data['room_no'])
            if room.occupied < room.capacity:
                if student.room:
                    old_room = student.room
                    old_room.occupied -= 1
                    old_room.save()
                student.room = room
                student.save()
                room.occupied += 1
                room.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'msg': 'Room is full'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)})

@csrf_exempt
def deallocate_room(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Admins only")

    if request.method == 'POST':

        student = Student.objects.get(id=id)

        if student.room:

            room = student.room

            room.occupied -= 1
            room.save()

            student.room = None
            student.save()

        return JsonResponse({'status': 'success'})

@csrf_exempt
def add_fee(request):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        student = Student.objects.get(id=data['student_id'])
        Fee.objects.create(student=student, amount=data['amount'], month=data['month'], status='Pending')
        return JsonResponse({'status': 'success'})

@csrf_exempt
def pay_fee(request, id):
    if request.method == 'POST':
        fee = Fee.objects.get(id=id)
        fee.status = 'Paid'
        fee.date_paid = timezone.now().date()
        fee.save()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def add_complaint(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student = Student.objects.first() # Mocking current user for frontend form
        if student:
            Complaint.objects.create(student=student, category=data['category'], description=data['desc'])
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'msg': 'No student found'}, status=400)

@csrf_exempt
def resolve_complaint(request, id):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    if request.method == 'POST':
        Complaint.objects.filter(id=id).update(status='Resolved')
        return JsonResponse({'status': 'success'})

@csrf_exempt
def mark_attendance(request):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        student = Student.objects.get(id=data['student_id'])
        Attendance.objects.update_or_create(
            student=student, 
            date=timezone.now().date(), 
            defaults={'status': data['status']}
        )
        return JsonResponse({'status': 'success'})

@csrf_exempt
def add_notice(request):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    if request.method == 'POST':
        data = json.loads(request.body)
        Notice.objects.create(title=data['title'], content=data['content'])
        return JsonResponse({'status': 'success'})



# CSV REPORTS
def report_students(request):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Room No', 'Joined On'])
    for s in Student.objects.all():
        writer.writerow([s.id, s.name, s.email, s.phone, s.room.room_no if s.room else 'None', s.created_at.date()])
    return response

def report_rooms(request):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rooms_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Room No', 'Type', 'Capacity', 'Occupied', 'Status'])
    for r in Room.objects.all():
        writer.writerow([r.room_no, r.room_type, r.capacity, r.occupied, r.status])
    return response

def report_fees(request):
    if not request.user.is_superuser:
     return HttpResponseForbidden("Admins only")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fees_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Fee ID', 'Student', 'Amount', 'Month', 'Status', 'Date Paid'])
    for f in Fee.objects.all():
        writer.writerow([f.id, f.student.name, f.amount, f.month, f.status, f.date_paid or 'Not Paid'])
    return response
