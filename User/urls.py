from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('hostel/signup/', views.hostel_admin_signup, name='hostel_admin_signup'),
    path('login/', views.login_view, name='login'),
    path('profile/update/', views.update_profile, name='profile_update'),
    path('profile/', views.profile, name='profile_detail'),
    path('logout/', views.custom_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
     path('hostel-admin/edit/<int:admin_id>/', views.edit_hostel_admin, name='hostel_admin_edit'),
    path('get-hostels-for-university/', views.get_hostels_for_university, name='get_hostels_for_university'),
    # Add more URLs as needed for student profiles, hostel admin dashboard, etc.
]
