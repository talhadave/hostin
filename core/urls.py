from django.urls import path
from . import views

urlpatterns = [
    # University URLs
    path('universities/', views.university_list, name='university_list'),

    # Hostel URLs
    path('', views.hostel_list, name='hostel_list'),
    path('hostels/create/', views.hostel_create, name='hostel_create'),
    path('hostels/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),
    path('hostels/<int:hostel_id>/update/', views.hostel_update, name='hostel_update'),
    path('hostels/<int:hostel_id>/delete/', views.hostel_delete, name='hostel_delete'),
    path('booking-requests/', views.booking_requests, name='booking_requests'),
    path('approve-booking/<int:booking_request_id>/', views.approve_booking, name='approve_booking'),
    path('reject-booking/<int:booking_request_id>/', views.reject_booking, name='reject_booking'),

    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/<int:hostel_id>/', views.room_create, name='room_create'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/update/', views.room_update, name='room_update'),
    path('rooms/<int:room_id>/delete/', views.room_delete, name='room_delete'),
]
