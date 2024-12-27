from django.urls import path, include

# Import views from the booking app
from booking import views

# Define booking-specific URL patterns
booking_urls = [
    # URL for creating a booking
    path('create/', views.create_booking, name='create_booking'),

    # URL for listing all bookings
    path('list/', views.get_all_bookings, name='get_all_bookings'),

    # URL for generating a PDF for a specific booking
    path('pdf/', views.generate_booking_pdf, name='generate_booking_pdf'),
]

# Main URL configuration
urlpatterns = [
    # Prefix all booking-related URLs with '/bookings' using the include() function
    path('bookings/', include((booking_urls, 'booking'))),
]
