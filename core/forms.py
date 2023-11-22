from typing import Any
from django import forms
from .models import Hostel, rooms,Feedback
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.widgets import TextInput,SelectMultiple
 

class HostelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        
        # Change the widget of 'embedCode' to a TextInput to make it smaller
        self.fields['embedCode'].widget = TextInput(attrs={
            'class': 'form-control rounded-pill',  # Maintain the same styling
            'placeholder': 'Embed Code'  # Set a placeholder
        })

    class Meta:
        model = Hostel
        fields = ('university', 'hostel_name', 'hostel_adress', 'picture', 'services', 'embedCode')


class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Extract hostel_id from kwargs with a default of None
        hostel_id = kwargs.pop('hostel_id', None)
        super(RoomForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control rounded-pill"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        
        # Only set self.hostel_id if it's provided
        if hostel_id is not None:
            self.hostel_id = hostel_id
            # If needed, modify the form fields here based on hostel_id

    def _get_room_list(self):
        # Ensure self.hostel_id is set before using it
        if hasattr(self, 'hostel_id'):
            return Hostel.objects.filter(pk=self.hostel_id).values_list('rooms__room_type', flat=True)
        return []

    def clean_room_type(self):
        room_type = self.cleaned_data.get("room_type")
        existing_room_types = self._get_room_list()
    
     # Exclude the current room's type from the check if we are updating
        if self.instance.pk:  # self.instance is the room being updated
            existing_room_types = existing_room_types.exclude(pk=self.instance.pk)
    
        if room_type in existing_room_types:
            raise forms.ValidationError("Room type already exists.")
        return room_type

    class Meta:
        model = rooms  # Ensure this is the correct model
        fields = ('room_type', 'room_price', 'services')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

    rating = forms.IntegerField(
        validators=[
            MinValueValidator(1, message='Rating should be at least 1.'),
            MaxValueValidator(5, message='Rating should be at most 5.')
        ],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5})
    )