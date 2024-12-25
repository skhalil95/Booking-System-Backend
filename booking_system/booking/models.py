from django.db import models
from datetime import timedelta
import os

class Booking(models.Model):
    name = models.CharField(max_length=255)
    civil_id = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def end_time(self):
        duration_minutes = int(os.getenv('BOOKING_DURATION', 60))
        return self.start_time + timedelta(minutes=duration_minutes)

    def __str__(self):
        return f"Booking for {self.name} at {self.start_time}"
