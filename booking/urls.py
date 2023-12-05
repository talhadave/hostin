from django.urls import path
from . import views
from core.views import hostel_list,search_hostels
urlpatterns = [
    # Other URL patterns
    path('', hostel_list, name='hostel_list_for_student'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-status/', views.booking_status, name='booking_status'),
    path('search/', search_hostels, name='search_hostels'),
    # path('checkout/<int:room_id>/', views.create_checkout_session, name='create_checkout_session'),
    # path('hostel-detail/<int:hostel_id>/', views.hostel_detail_for_student, name='hostel_detail_for_student'),
]
