from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-booking/', create_booking, name='create_booking'),
    path('get-bookings/', get_all_bookings, name='get_all_bookings'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
