from django.shortcuts import render, redirect, get_object_or_404
from .models import University, Hostel, rooms
from .forms import HostelForm, RoomForm,FeedbackForm
from django.contrib.auth.decorators import login_required
from .models import Hostel, University,Hostel
from booking.models import Booking
from .models import Hostel  # Import the Hostel model
from django.urls import reverse_lazy


def university_list(request):
    universities = University.objects.all()
    return render(request, 'university_list.html', {'universities': universities})

@login_required(login_url="/User/")
def hostel_list(request):
    if hasattr(request.user, 'hosteladmin'):
        # User is an admin, retrieve admin-specific data
        admin_hostels = Hostel.objects.filter(ownerUser=request.user)
        student_hostels = None
    else:
        # User is a student, retrieve student-specific data
        admin_hostels = None
        student_hostels = Hostel.objects.filter(university__name=request.user.student.university_name)

    context = {
        'admin_hostels': admin_hostels,
        'student_hostels': student_hostels,
    }

    return render(request, 'hostel_list.html', context)


def room_list(request):
    rooms_data = rooms.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms_data})


def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    services = hostel.services.all()
    feedback= hostel.feedback_set.all()
    return render(request, 'hostel_detail.html', {'hostel': hostel,"services":services})

def room_detail(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    bookings = Booking.objects.filter(room=room)  # Get all bookings for this room
    booked_students = [booking.student for booking in bookings]
    return render(request, 'room_detail.html', {'room': room,'booked_students': booked_students})

def hostel_create(request):
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.ownerUser = request.user  # Assuming you want to set the owner to the currently logged-in user
            hostel.save()
            return redirect('hostel_list')
    else:
        form = HostelForm()   
    return render(request, 'hostel_form.html', {'form': form})

def room_create(request, hostel_id):
    # Get the hostel instance using the provided hostel_id

    if request.method == 'POST':
        hostel = Hostel.objects.get(pk=hostel_id)
        form = RoomForm(hostel_id=hostel_id, data=request.POST, files=request.FILES)
        
        if form.is_valid():
            room = form.save(commit=False)
            room.hostel = hostel  # Associate the room with the hostel
            room.save()
            return redirect(reverse_lazy('hostel_detail', kwargs={"hostel_id":hostel_id}))
    else:
        form = RoomForm(hostel_id=hostel_id)
    
    return render(request, 'room_form.html', {'form': form})

def hostel_update(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES, instance=hostel)
        if form.is_valid():
            form.save()
            return redirect('hostel_list')
    else:
        form = HostelForm(instance=hostel)
    
    return render(request, 'hostel_form.html', {'form': form})


def room_update(request, room_id):
    room = get_object_or_404(rooms, id=room_id)  # Make sure 'Room' is your model class name
    hostel_id = room.hostel.id  # Assuming the Room model has a 'hostel' foreign key

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room, hostel_id=hostel_id)
        if form.is_valid():
            form.save()
            return redirect('room_detail',room_id=room.id)
    else:
        form = RoomForm(instance=room, hostel_id=hostel_id)

    return render(request, 'room_form.html', {'form': form})


def hostel_delete(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == 'POST':
        hostel.delete()
        return redirect('hostel_list')
    
    return render(request, 'hostel_delete.html', {'hostel': hostel})

def room_delete(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    
    return render(request, 'room_delete.html', {'room': room})


def booking_requests(request):
    # Retrieve booking requests that need approval
    booking_requests = Booking.objects.filter(status='Pending')
    return render(request, 'booking_requests.html', {'booking_requests': booking_requests})

def approve_booking(request, booking_request_id):
    booking_request = get_object_or_404(Booking, id=booking_request_id)
    
    # Approve the booking request (update status to 'Approved')
    booking_request.status = 'Approved'
    booking_request.save()
    
    # You can add further logic, such as sending notifications to the student
    
    return redirect('booking_requests')

def reject_booking(request, booking_request_id):
    booking_request = get_object_or_404(Booking, id=booking_request_id)
    
    # Reject the booking request (update status to 'Rejected')
    booking_request.status = 'Rejected'
    booking_request.save()
    
    # You can add further logic, such as sending notifications to the student
    
    return redirect('booking_requests')



@login_required
def search_hostels(request):
    search_query = request.GET.get('q')
    if search_query:
        universities = University.objects.filter(name__icontains=search_query)
    else:
        universities = None

    # if search_query:
    #     # Check if the search query is a university name
    #     university = University.objects.filter(name__icontains=search_query).first()

    #     if university:
    #         # If a university is found, get hostels associated with that university
    #         hostels = Hostel.objects.filter(university=university)
    #     else:
    #         # If no university is found, search hostels by hostel name
    #         hostels = Hostel.objects.filter(hostel_name__icontains=search_query)

    context = {
        'universities': universities,
    }

    return render(request, 'search_hostels.html', context)


# views.py

from django.shortcuts import get_object_or_404, redirect, render
from .models import Services

def service_remove(request, hostel_id, service_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    service = get_object_or_404(Services, id=service_id)

    if request.method == 'POST':
        # If the request method is POST, delete the service and redirect to hostel_detail.
        service.delete()
        return redirect('hostel_detail', hostel_id=hostel.id)  # Pass hostel.id in the redirect URL.

    return render(request, 'service_remove.html', {'service': service, 'hostel': hostel})



def feedback(request, hostel_id):
    hostel = Hostel.objects.get(pk=hostel_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assuming you have user authentication
            feedback.hostel = hostel
            feedback.save()
            return redirect('hostel_detail', hostel_id=hostel_id)

    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form, 'hostel': hostel})
