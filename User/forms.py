# forms.py
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Student, HostelAdmin
from core.models import University



class StudentSignupForm(UserCreationForm):
    university_name = forms.ModelChoiceField(
        queryset=University.objects.all(),
        empty_label="Select your university"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','university_name']



class HostelAdminSignupForm(UserCreationForm):
    university_name = forms.ModelChoiceField(
        queryset=University.objects.all(),
        empty_label="Select your university"
    ) # Add the university_name field
    Hostel_name = forms.CharField(max_length=100) 
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2', 'university_name','Hostel_name')

# forms.py
from django import forms

class StudentLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# forms.py
from django import forms

class HostelAdminLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


