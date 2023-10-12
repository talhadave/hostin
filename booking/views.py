from django.shortcuts import render, redirect, get_object_or_404
from core.models import Hostel, rooms,University
from .forms import BookingForm
from User.models import Student


def hostel_list_for_student(request):
    # Get hostels based on the student's university
    user_university = request.user.student.university_name
    # user_university = request.user.student.university_name
    university = University.objects.get(name=user_university)
    hostels = Hostel.objects.filter(university=university)
    print(hostels)
    return render(request, 'hostel_list_for_student.html', {'hostels': hostels})

def hostel_detail_for_student(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms_available = rooms.objects.filter(hostel=hostel)
    return render(request, 'hostel_detail_for_student.html', {'hostel': hostel, 'rooms_available': rooms_available})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm
from .models import rooms
from django.shortcuts import render, redirect, get_object_or_404
from .models import rooms
from .forms import BookingForm

def book_room(request, room_id):
    room = get_object_or_404(rooms, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.status = 'Pending'
            booking.save()
            # Notify hostel admin (implement notifications later)
            return redirect('student_dashboard')  # Redirect to success page or bookings list

    else:
        form = BookingForm()

    return render(request, 'book_room.html', {'form': form, 'room': room})


from django.shortcuts import render
from .models import Booking

def booking_status(request):
    # Get the bookings of the currently logged-in student
    student_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_status.html', {'student_bookings': student_bookings})
