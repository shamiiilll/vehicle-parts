from django.shortcuts import render
from django.db.models import Sum, F
from .models import Student, Room, Fee, Complaint  # Adjust import based on your app name

def dashboard_view(request):
    """
    Dashboard view that calculates real-time stats from the MySQL database.
    """
    
    # 1. TOTAL STUDENTS: Count total records from "students" table
    students_count = Student.objects.count()
    
    # 2. TOTAL ROOMS: Count total rooms from "rooms" table
    total_rooms = Room.objects.count()
    
    # 3. AVAILABLE ROOMS: Calculate rooms where occupancy < capacity
    available_rooms = Room.objects.filter(occupancy__lt=F('capacity')).count()
    
    # 4. OCCUPANCY RATE: (Total occupied beds / Total capacity) * 100
    totals = Room.objects.aggregate(
        total_capacity=Sum('capacity'),
        total_occupied=Sum('occupancy')
    )
    
    total_capacity = totals['total_capacity'] or 1  # prevent division by zero
    total_occupied = totals['total_occupied'] or 0
    occupancy_rate = (total_occupied / total_capacity) * 100 if total_capacity > 0 else 0
    
    # 5. PENDING FEES: Count fees where fee status = "Pending" or "Overdue"
    # Assuming Fee model has a related student and status field
    pending_fees = Fee.objects.filter(status__in=['Pending', 'Overdue']).count()
    
    # 6. COMPLAINTS: Count complaints where status = "Pending"
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    
    # Pass all variables to the template context
    context = {
        'students_count': students_count,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupancy_rate': occupancy_rate,
        'pending_fees': pending_fees,
        'pending_complaints': pending_complaints,
    }
    
    return render(request, 'dashboard.html', context)
