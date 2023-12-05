from typing import Any
from django import forms
from .models import Hostel, rooms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.widgets import TextInput, SelectMultiple


class HostelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
            if visible.field.label == "Services":
                visible.field.widget.attrs["rows"] = "5"

        # Change the widget of 'embedCode' to a TextInput to make it smaller
        self.fields["embedCode"].widget = TextInput(
            attrs={
                "class": "form-control",  # Maintain the same styling
                "placeholder": "Embed Code",  # Set a placeholder
            }
        )

    # services = forms.ModelMultipleChoiceField(
    #     queryset=Services.objects.all(),
    #     widget=forms.CheckboxSelectMultiple(attrs={'id': 'custom_services_id'})
    # )
    class Meta:
        model = Hostel
        fields = (
            "university",
            "hostel_type",
            "hostel_name",
            "hostel_adress",
            "picture",
            "services",
            "embedCode",
        )


class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Extract hostel_id from kwargs with a default of None
        super(RoomForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
            if visible.field.label == "Services":
                visible.field.widget.attrs["rows"] = "5"

    class Meta:
        model = rooms  # Ensure this is the correct model
        fields = ("room_type", "floor", "room_price", "picture", "services")


