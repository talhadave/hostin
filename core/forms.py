from typing import Any
from django import forms
from .models import Hostel, rooms

 

class HostelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label

    class Meta:
        model = Hostel
        fields = ('university', 'hostel_name', 'hostel_adress', 'picture')

class RoomForm(forms.ModelForm):
    def __init__(self, hostel_id, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"]= visible.field.label
        self.hostel_id = hostel_id

    def _get_room_list(self):
        return Hostel.objects.filter(pk=self.hostel_id).values_list('rooms__room_number', flat=True)
        
    def clean_room_number(self):
        room_number =self.data.get("room_number")
        if room_number in self._get_room_list():
                raise forms.ValidationError("Room number already exists.")
        return room_number
    
    class Meta:
        model = rooms
        fields = ('room_number', 'room_price', 'picture')
