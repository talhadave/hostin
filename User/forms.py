# forms.py
from typing import Any
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Student, HostelAdmin
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

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','university_name']



class HostelAdminSignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

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


