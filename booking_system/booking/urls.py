from django.urls import path
from .views import *

urlpatterns = [
    path('create-booking/', create_booking, name='create_booking'),
    path('get-bookings/', get_all_bookings, name='get_all_bookings'),
]

