from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import main_views as views

urlpatterns = [
    path('',views.home,name='home'),
    path('hostel/', include('core.urls')),
    path('User/', include('User.urls')),
    path('booking/', include('booking.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
