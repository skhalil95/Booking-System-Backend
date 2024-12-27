from rest_framework import serializers
from booking.models import Booking
from datetime import datetime, timedelta, timezone
from django.conf import settings


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Handles validation and formatting of booking fields.
    """
    # Name field with custom error message for the 'required' validation
    name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'The name field is required.'
        }
    )

    # Civil ID field with regex validation for exactly 12 digits and custom error messages
    civil_id = serializers.RegexField(
        regex=r'^\d{12}$',
        required=True,
        error_messages={
            'invalid': 'Civil ID must be exactly 12 digits.',
            'required': 'The civil_id field is required.'
        }
    )

    # Start time field with specific format requirements and custom error messages
    start_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",  # Output format
        input_formats=["%Y-%m-%d %H:%M"],  # Accepted input formats
        required=True,
        error_messages={
            'invalid': 'Invalid start_time format. Use YYYY-MM-DD HH:MM.',
            'required': 'The start_time field is required.'
        }
    )

    # Computed field for end time
    end_time = serializers.SerializerMethodField()

    class Meta:
        # Define the model and fields to include in the serialized output
        model = Booking
        fields = ['id', 'name', 'civil_id', 'start_time', 'end_time', 'qr_code', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_start_time(self, value):
        """
        Custom validation for the start_time field.
        Ensures the time is in the future and within the allowed booking window.
        """
        current_time = datetime.now(tz=timezone.utc)

        # Ensure the start time is not in the past
        if value < current_time and not (
                value <= current_time <= value + timedelta(minutes=settings.BOOKING_DURATION - 1)):
            raise serializers.ValidationError("Booking can only be made for future time slots.")

        # Check if the booking time is within the allowed hours
        if not (settings.BOOKING_STARTING_WINDOW_TIME <= value.hour < settings.BOOKING_ENDING_WINDOW_TIME):
            raise serializers.ValidationError("Bookings can only be made between 9:00 AM and 4:00 PM.")

        return value

    def get_end_time(self, obj):
        """
        Calculates and formats the end_time based on start_time and booking duration.
        This method is used for the SerializerMethodField.
        """
        duration_minutes = settings.BOOKING_DURATION
        end_time = obj.start_time + timedelta(minutes=duration_minutes)
        return end_time.strftime("%Y-%m-%d %H:%M")
