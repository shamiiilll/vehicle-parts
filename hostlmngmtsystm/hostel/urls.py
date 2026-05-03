from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('rooms/', views.rooms_page),
    path('students/', views.students_page),
    path('fees/', views.fees_page),
    path('complaints/', views.complaints_page),
    path('logout/', views.logout_page, name='logout'),

    
    path('api/data/', views.api_data, name='api_data'),
    path('api/add_student/', views.add_student, name='add_student'),
    path('api/delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('api/add_room/', views.add_room, name='add_room'),
    path('api/delete_room/<str:no>/', views.delete_room, name='delete_room'),
    path('api/allocate_room/', views.allocate_room, name='allocate_room'),
    path('api/deallocate_room/<int:id>/', views.deallocate_room, name='deallocate_room'),
    path('api/add_complaint/', views.add_complaint, name='add_complaint'),
    path('api/resolve_complaint/<int:id>/', views.resolve_complaint, name='resolve_complaint'),
    path('api/add_fee/', views.add_fee, name='add_fee'),
    path('api/pay_fee/<int:id>/', views.pay_fee, name='pay_fee'),
    path('api/mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('api/add_notice/', views.add_notice, name='add_notice'),
    path('reports/students/', views.report_students, name='report_students'),
    path('reports/rooms/', views.report_rooms, name='report_rooms'),
    path('reports/fees/', views.report_fees, name='report_fees'),
]
