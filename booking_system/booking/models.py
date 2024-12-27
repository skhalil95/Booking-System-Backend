from django.db import models

class Booking(models.Model):
    """
    Model representing a booking.
    Includes fields for user details, booking time, and QR code,
    along with timestamps for creation and updates.
    """
    # Name of the person booking (up to 255 characters)
    name = models.CharField(max_length=255)

    # Civil ID of the person (stored as a big integer for large IDs)
    civil_id = models.BigIntegerField()

    # Start time of the booking (required)
    start_time = models.DateTimeField()

    # QR code for the booking, stored as an image file (optional)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    # Timestamp for when the booking was created (auto-filled)
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp for when the booking was last updated (auto-updated)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the booking.
        Useful for debugging or when displaying the object in the Django admin.
        """
        return f"Booking for {self.name} at {self.start_time}"
