from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy

from .forms import (StudentSignupForm, HostelAdminSignupForm, LoginForm, HostelAdminEditForm,
                    StudentLoginForm, HostelAdminLoginForm,
                    UserUpdateForm, ProfileUpdateForm)
from .models import Student, HostelAdmin, Profile
from core.models import Hostel,University
from django.core.exceptions import ObjectDoesNotExist


def get_hostels_for_university(request):
    university_name = request.GET.get('university')
    hostels = Hostel.objects.filter(university__name=university_name).values('name', 'address')
    return JsonResponse(list(hostels), safe=False)


def landing_page(request):
    hostel_id = request.GET.get("hostel")
    university_id = request.GET.get("university")
    hostels = Hostel.objects.filter(id=hostel_id) if hostel_id else Hostel.objects.filter(university__id=university_id)

    all_hostels = Hostel.objects.all()
    all_universities = University.objects.all()
    context = {"hostels": hostels, "all_hostels": all_hostels, "all_universities": all_universities}
    return render(request, "landing_page.html", context)


def choice_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "choice.html")


def student_signup(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            student = Student(user=user, university_name=form.cleaned_data["university_name"])
            student.save()
            Profile.objects.get_or_create(student=student)
            login(request, user)
            return redirect("hostel_list")
    else:
        form = StudentSignupForm()
    return render(request, "signup.html", {"form": form})


def hostel_admin_signup(request):
    if request.method == "POST":
        form = HostelAdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            hostel_admin = HostelAdmin(user=user, contact_number=form.cleaned_data["contact_number"])
            hostel_admin.save()
            login(request, user)
            return redirect("hostel_list")
    else:
        form = HostelAdminSignupForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user:
                login(request, user)
                return redirect(request.POST.get("next") or "hostel_list")
        return render(request, "choice.html", {"login_form": form, "error": "Invalid User credentials"})
    else:
        form = LoginForm()
    return render(request, "choice.html", {"login_form": form, "next": request.GET.get("next")})




@login_required(login_url="/login/")
def profile(request):
    return render(request, "profile_detail.html")


@login_required(login_url="/login/")
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.student.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile_detail")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.student.profile)
    return render(request, "profile_update.html", {"user_form": user_form, "profile_form": profile_form})


@login_required(login_url="/login/")
def custom_logout(request):
    logout(request)
    return redirect(reverse("login"))




@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('hostel_list')
        messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def edit_hostel_admin(request, admin_id):
    hostel_admin = get_object_or_404(HostelAdmin, id=admin_id)
    user = hostel_admin.user

    if request.method == 'POST':
        form = HostelAdminEditForm(request.POST, instance=hostel_admin)
        if form.is_valid():
            form.save()
            return redirect("hostel_list")
    else:
        form = HostelAdminEditForm(instance=hostel_admin)

    return render(request, 'edit_hostel_admin.html', {'form': form})
