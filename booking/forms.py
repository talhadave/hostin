# forms.py
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    contact_number = forms.CharField(label="Contact Number", max_length=15)

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
            if visible.field.label == "Description":
                visible.field.widget.attrs["rows"] = "4"
                visible.field.widget.attrs["required"] = True
               

    class Meta:
        model = Booking
        fields = ["contact_number", "cnic", "description"]
