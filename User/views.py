# views.py
from django.contrib.auth import logout,login, authenticate
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse 
from .forms import StudentSignupForm, HostelAdminSignupForm, LoginForm
from .models import Student, HostelAdmin,Profile
from django.http import HttpResponse
from .forms import StudentLoginForm, HostelAdminLoginForm,UserUpdateForm, ProfileUpdateForm
from django.core.exceptions import ObjectDoesNotExist

def choice_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect already authenticated users to the home page or dashboard
    return render(request, 'choice.html')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            university_name = form.cleaned_data['university_name']
            user = form.save()
            student = Student(user=user, university_name=university_name)
            student.save()
            Profile.objects.get_or_create(student=student) 
            login(request, user)
            return redirect('hostel_list_for_student')
    else:
        form = StudentSignupForm()
    return render(request, 'signup.html', {'form': form})


def hostel_admin_signup(request):
    if request.method == 'POST':
        form = HostelAdminSignupForm(request.POST)
        if form.is_valid():
            contact_number = form.cleaned_data["contact_number"]
            user = form.save()
            hostel_admin = HostelAdmin(user=user, contact_number=contact_number)
            hostel_admin.save()
            login(request, user)
            return redirect('hostel_list')  # Redirect to the hostel admin dashboard
    else:
        form = HostelAdminSignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        error =None
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    user.student
                    role = "student"
                except Student.DoesNotExist:
                    user.hosteladmin
                    role = "hosteladmin"
                except HostelAdmin.DoesNotExist:
                    role = None
                if role is "student":
                    login(request, user)
                    return redirect('hostel_list_for_student')
                elif role is "hosteladmin":
                    login(request, user)
                    return redirect('hostel_list')
                else:
                    error = "User has no access"
            else:
                error = "Invalid User credentials"
        else:
            error = "Error in Form"
        return render(request, 'choice.html', {"login_form": form, "error": error})
    else:
        form = LoginForm()

    return render(request, 'choice.html' , {"login_form": form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    student = user.student
                    login(request, user)
                    return redirect('hostel_list_for_student')
                except ObjectDoesNotExist:
                    # Student with this username does not exist, show an error message
                    form.add_error(None, 'Invalid student credentials')
        else:
            # Form is not valid, handle the error
            return render(request, 'choice.html', {'student_form': form, 'hostel_admin_form': HostelAdminLoginForm()})

    else:
        form = StudentLoginForm()

    return render(request, 'choice.html', {'student_form': form, 'hostel_admin_form': HostelAdminLoginForm()})

def hostel_admin_login(request):
    if request.method == 'POST':
        form = HostelAdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    hostel_admin = user.hosteladmin
                    login(request, user)
                    return redirect('hostel_list')
                except ObjectDoesNotExist:
                    # Hostel admin with this username does not exist, show an error message
                    form.add_error(None, 'Invalid hostel admin credentials')
        else:
            # Form is not valid, handle the error
            return render(request, 'choice.html', {'student_form': StudentLoginForm(), 'hostel_admin_form': form})

    else:
        form = HostelAdminLoginForm()

    return render(request, 'choice.html', {'student_form': StudentLoginForm(), 'hostel_admin_form': form})

def profile(request):
    # This view assumes you have a 'profile_detail.html' template
    return render(request, 'profile_detail.html')


def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.student.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Redirect to a success page, such as the profile detail view
            return redirect('profile_detail')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.student.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'profile_update.html', context)



def custom_logout(request):
    logout(request)
    return redirect(reverse('login'))



def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='student').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Permission Denied", status=403)  # Customize the response as needed

    return _wrapped_view



def hostelAdmin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='hosteladmin').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Permission Denied", status=403)  # Customize the response as needed

    return _wrapped_view


def view_student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    profile = student.profile
    return render(request, 'student_profile.html', {'student': student, 'profile': profile})