from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.choice_page, name='choice_page'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('hostel-admin/signup/', views.hostel_admin_signup, name='hostel_admin_signup'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('hostel-admin/dashboard/', views.hostel_admin_dashboard, name='hostel_admin_dashboard'),
    path('student/login/', views.student_login, name='student_login'),
    path('hostel-admin/login/', views.hostel_admin_login, name='hostel_admin_login'),
    path('logout/', views.custom_logout, name='logout'),
    # Add more URLs as needed for student profiles, hostel admin dashboard, etc.
]
