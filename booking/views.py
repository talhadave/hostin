from django.shortcuts import render, redirect, get_object_or_404
from core.models import Hostel, rooms
from .forms import BookingForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .models import rooms
from User.models import Student
import time


def hostel_list_for_student(request):
    # Get hostels based on the student's university
    user_university = request.user.student.university_name
    hostels = Hostel.objects.filter(university__name=user_university)
    return render(request, 'hostel_list_for_student.html', {'hostels': hostels})

def hostel_detail_for_student(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    return render(request, 'hostel_detail_for_student.html', {'hostel': hostel})

def book_room(request, room_id):
    room = get_object_or_404(rooms, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.student
            booking.room = room
            booking.status = 'Pending'
            booking.save()
            # Notify hostel admin (implement notifications later)
            return redirect('booking_status')  # Redirect to success page or bookings list

    else:
        form = BookingForm()

    return render(request, 'book_room.html', {'form': form, 'room': room})


from django.shortcuts import render
from .models import Booking

def booking_status(request):
    # Get the bookings of the currently logged-in student
    try:
        student = request.user.student
        student_bookings = Booking.objects.filter(student=student)
    except Student.DoesNotExist:
        student_bookings = []
    return render(request, 'booking_status.html', {'student_bookings': student_bookings})
