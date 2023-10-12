from django import forms
from .models import Hostel, rooms

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ('university', 'hostel_name', 'hostel_adress', 'date', 'picture')

class RoomForm(forms.ModelForm):
    class Meta:
        model = rooms
        fields = ('room_number', 'room_price', 'hostel', 'picture')
