
from rest_framework import serializers
from booking.models import Booking
from datetime import datetime, timedelta, timezone
from django.conf import settings


class BookingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
            'required': 'The name field is required.'
        })
    civil_id = serializers.RegexField(
        regex=r'^\d{12}$',
        required=True,
        error_messages={
            'invalid': 'Civil ID must be exactly 12 digits.',
            'required': 'The civil_id field is required.'
        })
    start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",  # Format for output
        input_formats=["%Y-%m-%d %H:%M"],  # Accepted input formats
        required=True,
        error_messages={
            'invalid': 'Invalid start_time format. Use YYYY-MM-DD HH:MM.',
            'required': 'The start_time field is required.'
        })

    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'name', 'civil_id', 'start_time', 'end_time', 'qr_code']


    def validate_start_time(self, value):
        current_time = datetime.now(tz=timezone.utc)
        if value < current_time and not (
                    value <= current_time <= value + timedelta(minutes=settings.BOOKING_DURATION - 1)):

            raise serializers.ValidationError("Booking can only be made for future time slots.")

        if not (settings.BOOKING_STARTING_WINDOW_TIME <= value.hour < settings.BOOKING_ENDING_WINDOW_TIME):
            raise serializers.ValidationError("Bookings can only be made between 9:00 AM and 4:00 PM.")

        return value

    def get_end_time(self, obj):
        """Calculate and format the end_time based on start_time and booking duration."""
        duration_minutes = settings.BOOKING_DURATION  # Default to 60 minutes
        end_time = obj.start_time + timedelta(minutes=duration_minutes)
        return end_time.strftime("%Y-%m-%d %H:%M")



