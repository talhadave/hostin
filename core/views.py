from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Min

from .models import University, Hostel, rooms
from booking.models import Booking
from .forms import HostelForm, RoomForm



# Hostel List View
def hostel_list(request):
    if hasattr(request.user, "hosteladmin"):
        hostels = Hostel.objects.filter(ownerUser=request.user)
    elif hasattr(request.user, "student"):
        hostels = Hostel.objects.filter(university__name=request.user.student.university_name)
    else:
        hostels = Hostel.objects.all().annotate(min_room_price=Min("room__room_price")).order_by("min_room_price")
    return render(request, "hostel_list.html", {"hostels": hostels})



# Hostel Detail View
@login_required(login_url="/login/")
def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    return render(request, "hostel_detail.html", {"hostel": hostel})

# Room Detail View
def room_detail(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    bookings = Booking.objects.filter(room=room)
    booked_students = [booking.student for booking in bookings]
    return render(request, "room_detail.html", {"room": room, "booked_students": booked_students})

# Hostel Create View
@login_required(login_url="/login/")
def hostel_create(request):
    if request.method == "POST":
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.ownerUser = request.user
            hostel.save()
            return redirect("hostel_list")
    else:
        form = HostelForm()
    return render(request, "hostel_form.html", {"form": form})

# Room Create View
@login_required(login_url="/login/")
def room_create(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    if request.method == "POST":
        form = RoomForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hostel = hostel
            room.save()
            return redirect(reverse_lazy("hostel_detail", kwargs={"hostel_id": hostel_id}))
    else:
        form = RoomForm()
    return render(request, "room_form.html", {"form": form})

# Hostel Update View
@login_required(login_url="/login/")
def hostel_update(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == "POST":
        form = HostelForm(request.POST, request.FILES, instance=hostel)
        if form.is_valid():
            form.save()
            return redirect("hostel_list")
    else:
        form = HostelForm(instance=hostel)
    return render(request, "hostel_form.html", {"form": form})

# Room Update View
@login_required(login_url="/login/")
def room_update(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room_detail", room_id=room.id)
    else:
        form = RoomForm(instance=room)
    return render(request, "room_form.html", {"form": form})

# Hostel Delete View
@login_required(login_url="/login/")
def hostel_delete(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == "POST":
        hostel.delete()
        return redirect("hostel_list")
    return render(request, "hostel_delete.html", {"hostel": hostel})

# Room Delete View
@login_required(login_url="/login/")
def room_delete(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    if request.method == "POST":
        hostel_id = room.hostel.id
        room.delete()
        return redirect(reverse_lazy("hostel_detail", kwargs={"hostel_id": hostel_id}))
    return render(request, "room_delete.html", {"room": room})

# Booking Requests View
@login_required(login_url="/login/")
def booking_requests(request):
    bookings = Booking.objects.filter(room__hostel__ownerUser=request.user)
    context = {
        "pending": bookings.filter(status="Pending"),
        "accepted": bookings.filter(status="Approved"),
        "rejected": bookings.filter(status="Rejected"),
    }
    return render(request, "booking_requests.html", {"bookings": context})

# Approve Booking Request View
@login_required(login_url="/login/")
def approve_booking(request, booking_request_id):
    booking_request = get_object_or_404(Booking, id=booking_request_id)
    booking_request.status = "Approved"
    booking_request.save()
    return redirect("booking_requests")

# Reject Booking Request View
@login_required(login_url="/login/")
def reject_booking(request, booking_request_id):
    booking_request = get_object_or_404(Booking, id=booking_request_id)
    booking_request.status = "Rejected"
    booking_request.save()
    return redirect("booking_requests")

# Search Hostels View
@login_required(login_url="/login/")
def search_hostels(request):
    search_query = request.GET.get("q")
    universities = University.objects.filter(name__icontains=search_query) if search_query else None
    return render(request, "search_hostels.html", {"universities": universities})



