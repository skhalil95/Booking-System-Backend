from django.urls import path, include

# Booking-specific URLs
from booking import views

booking_urls = [
    path('create/', views.create_booking, name='create_booking'),
    path('list/', views.get_all_bookings, name='get_all_bookings'),
    path('pdf/', views.generate_booking_pdf, name='generate_booking_pdf'),
]

# Main URL patterns
urlpatterns = [
    path('bookings/', include((booking_urls, 'booking'))),  # Add a '/bookings' prefix
]
