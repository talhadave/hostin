from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # path('', views.choice_page, name='choice_page'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('hostel/signup/', views.hostel_admin_signup, name='hostel_admin_signup'),
    path('login/', views.login_view, name='login'),
    path('hostel/login/', views.hostel_admin_login, name='hostel_admin_login'),
    path('profile/update/', views.update_profile, name='profile_update'),
    path('profile/', views.profile, name='profile_detail'),
    path('students/profile/<int:student_id>/', views.view_student_profile, name='view_student_profile'),
    path('logout/', views.custom_logout, name='logout'),
    # Add more URLs as needed for student profiles, hostel admin dashboard, etc.
]
