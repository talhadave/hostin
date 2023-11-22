from django.contrib import admin
from .models import University,Hostel,rooms,Services
# Register your models here.
admin.site.register(University)
admin.site.register(Hostel)
admin.site.register(Services)
admin.site.register(rooms)