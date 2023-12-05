from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

from core.models import Hostel, rooms
from .forms import BookingForm
from .models import Booking
from User.models import Student

# Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY





@login_required(login_url="/login/")
def book_room(request, room_id):
    room = get_object_or_404(rooms, id=room_id)
    student = request.user.student
    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        booking, created = Booking.objects.get_or_create(room=room, student=student)
        print(booking.status)
        if created or booking.status == "Rejected":
            booking.description = form.cleaned_data["description"]
            booking.cnic = form.cleaned_data["cnic"]
            booking.status = "Pending"
            booking.save()
            if student.contact_number != form.cleaned_data["contact_number"]:
                student.contact_number = form.cleaned_data["contact_number"]
                student.save()
            return redirect(reverse('booking_status'))

    return render(request, "book_room.html", {"form": form, "room": room})


@login_required(login_url="/login/")
def booking_status(request):
    student_bookings = Booking.objects.filter(student=request.user.student)
    return render(request, "booking_status.html", {"student_bookings": student_bookings})


# @login_required(login_url="/login/")
# def create_checkout_session(request, room_id):
#     room = get_object_or_404(rooms, id=room_id)
#     session = stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         line_items=[{
#             "price_data": {
#                 "currency": "pkr",
#                 "product_data": {"name": room.hostel},
#                 "unit_amount":int(room.room_price * (30 / 100)),
#             },
#             "quantity": 1,
#         }],
#         mode="payment",
#         success_url=request.build_absolute_uri(reverse("booking_status")),
#         cancel_url=request.build_absolute_uri(reverse("book_room", args=[room_id])),
#     )
    
#     return redirect(session.url)

# @login_required(login_url="/login/")
# def hostel_list_for_student(request):
#     hostels = Hostel.objects.filter(university__name=request.user.student.university_name)
#     return render(request, "hostel_list_for_student.html", {"hostels": hostels})


# @login_required(login_url="/login/")
# def hostel_detail_for_student(request, hostel_id):
#     hostel = get_object_or_404(Hostel, id=hostel_id)
#     return render(request, "hostel_detail_for_student.html", {"hostel": hostel})

