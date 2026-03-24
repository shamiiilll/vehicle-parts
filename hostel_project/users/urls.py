from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rooms/', views.rooms, name='rooms'),
    path('fees/', views.fees, name='fees'),
    path('complaints/', views.complaints, name='complaints'),
    path('notices/', views.notices, name='notices'),
    path('students/', views.students, name='students'),
]