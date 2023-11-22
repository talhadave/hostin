# forms.py
from typing import Any
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Student, HostelAdmin,Profile
from core.models import University



class StudentSignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label


    university_name = forms.ModelChoiceField(
        queryset=University.objects.all(),
        empty_label="Select your university"
    )
    contact_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','university_name','contact_number']



class HostelAdminSignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label
    contact_number = forms.CharField(max_length=15, required=False)
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2','contact_number')

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

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'phone_number', 'occupation', 'address', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded-pill'
            if visible.name != 'profile_picture':
                visible.field.widget.attrs['placeholder'] = visible.field.label


