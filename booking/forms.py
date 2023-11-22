# forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date','user_info']
        widgets = {
            'user_info': forms.Textarea(attrs={'placeholder': 'Any additional information...'})
        }
