from django.shortcuts import render, redirect, get_object_or_404
from .models import University, Hostel, rooms
from .forms import HostelForm, RoomForm

def university_list(request):
    universities = University.objects.all()
    return render(request, 'university_list.html', {'universities': universities})

from django.shortcuts import render
from .models import Hostel
from django.contrib.auth.decorators import login_required

@login_required
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
    return render(request, 'hostel_detail.html', {'hostel': hostel})

def room_detail(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    return render(request, 'room_detail.html', {'room': room})

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

from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Hostel  # Import the Hostel model

def room_create(request, hostel_id):
    # Get the hostel instance using the provided hostel_id
    hostel = Hostel.objects.get(pk=hostel_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a room associated with the hostel
            room = form.save(commit=False)
            room.hostel = hostel  # Associate the room with the hostel
            room.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    
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
    room = get_object_or_404(rooms, id=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    
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


from django.shortcuts import render, redirect, get_object_or_404
from booking .models import Booking
from User.views import hostelAdmin_required


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


# from django.shortcuts import render
# from .models import Hostel, University
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import University, Hostel

# def search_hostels(request):
#     query = request.GET.get('q')
#     universities = University.objects.filter(name__icontains=query)
#     hostels = Hostel.objects.filter(hostel_name__icontains=query)

#     context = {
#         'universities': universities,
#         'hostels': hostels,
#         'query': query,
#     }

#     return render(request, 'search_hostels.html', context)


from django.shortcuts import render
from .models import Hostel, University
from django.contrib.auth.decorators import login_required

@login_required
def search_hostels(request):
    search_query = request.GET.get('q')

    universities = University.objects.all()
    hostels = None

    if search_query:
        # Check if the search query is a university name
        university = University.objects.filter(name__icontains=search_query).first()

        if university:
            # If a university is found, get hostels associated with that university
            hostels = Hostel.objects.filter(university=university)
        else:
            # If no university is found, search hostels by hostel name
            hostels = Hostel.objects.filter(hostel_name__icontains=search_query)

    context = {
        'universities': universities,
        'hostels': hostels,
    }

    return render(request, 'search_hostels.html', context)
