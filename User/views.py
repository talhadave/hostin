# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User  # Import the User model
from .forms import StudentSignupForm, HostelAdminSignupForm
from .models import Student, HostelAdmin
from django.http import HttpResponse

def choice_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect already authenticated users to the home page or dashboard
    return render(request, 'choice.html')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            university_name = form.cleaned_data['university_name']
            student = Student(user=user, university_name=university_name)
            student.save()
            login(request, user)
            return redirect('student_login')
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})


def hostel_admin_signup(request):
    if request.method == 'POST':
        form = HostelAdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            university_name = form.cleaned_data['university_name']
            hostel_admin = HostelAdmin(user=user, university_name=university_name)
            hostel_admin.save()
            login(request, user)
            return redirect('hostel_admin_dashboard')  # Redirect to the hostel admin dashboard
    else:
        form = HostelAdminSignupForm()
    return render(request, 'hostel_admin_signup.html', {'form': form})


# views.py
from django.shortcuts import render
from .models import HostelAdmin

def hostel_admin_dashboard(request):
    # Ensure the user is authenticated and is a hostel admin
    if request.user.is_authenticated and HostelAdmin.objects.filter(user=request.user).exists():
        hostel_admin = HostelAdmin.objects.get(user=request.user)
        return render(request, 'hostel_admin_dashboard.html', {'user': request.user, 'hostel_admin': hostel_admin})
    else:
        return redirect('choice_page')  # Redirect to the choice page if not authenticated or not a hostel admin
# views.py
from django.shortcuts import render
from .models import Student

def student_dashboard(request):
    # Ensure the user is authenticated and is a student
    if request.user.is_authenticated and Student.objects.filter(user=request.user).exists():
        student = Student.objects.get(user=request.user)
        return render(request, 'student_dashboard.html', {'user': request.user, 'student': student})
    else:
        return redirect('choice_page')  # Redirect to the choice page if not authenticated or not a student



# views.py
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import StudentLoginForm
from .models import Student
from django.core.exceptions import ObjectDoesNotExist
# views.py
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import StudentLoginForm, HostelAdminLoginForm
from django.core.exceptions import ObjectDoesNotExist

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

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

def custom_logout(request):
    logout(request)
    return redirect(reverse('choice_page'))



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