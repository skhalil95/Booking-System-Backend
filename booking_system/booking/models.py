from django.db import models
from datetime import timedelta
import os

class Booking(models.Model):
    """
    Model representing a booking.
    Includes fields for user details, booking time, and QR code.
    """
    # Name of the person booking (up to 255 characters)
    name = models.CharField(max_length=255)

    # Civil ID of the person (stored as a big integer for large IDs)
    civil_id = models.BigIntegerField()

    # Start time of the booking (required)
    start_time = models.DateTimeField()

    # QR code for the booking, stored as an image file (optional)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        """
        String representation of the booking.
        Useful for debugging or when displaying the object in the Django admin.
        """
        return f"Booking for {self.name} at {self.start_time}"

