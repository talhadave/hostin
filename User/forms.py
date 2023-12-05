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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).first():
            raise forms.ValidationError("email already exist")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','university_name']



class HostelAdminSignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label
    contact_number = forms.CharField(label="Contact Number", max_length=15, required=False)
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        if HostelAdmin.objects.filter(contact_number__iexact=contact_number).first():
            raise forms.ValidationError("contact no already exist")
        return contact_number
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2','contact_number')

# forms.py
from django import forms

class LoginForm(forms.Form):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

class StudentLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# forms.py
from django import forms

class HostelAdminLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded-pill'
            visible.field.widget.attrs['placeholder'] = visible.field.label

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
            if visible.field.label != 'Profile picture':
                visible.field.widget.attrs['placeholder'] = visible.field.label


class HostelAdminEditForm(forms.ModelForm):
    class Meta:
        model = HostelAdmin
        fields = ['contact_number']

    def __init__(self, *args, **kwargs):
        super(HostelAdminEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded-pill'

    def save(self, commit=True):
        hostel_admin = super(HostelAdminEditForm, self).save(commit=False)

        if commit:
            hostel_admin.save()
        return hostel_admin
        

