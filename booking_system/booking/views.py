import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta
import io
import qrcode
from django.core.files.base import ContentFile
from booking.models import Booking

# Swagger parameters
from django.conf import settings

name_param = openapi.Parameter(
    'name', openapi.IN_BODY, description="Name of the user", type=openapi.TYPE_STRING, required=True
)
civil_id_param = openapi.Parameter(
    'civil_id', openapi.IN_BODY, description="Civil ID of the user", type=openapi.TYPE_STRING, required=True
)
start_time_param = openapi.Parameter(
    'start_time', openapi.IN_BODY, description="Start time in format YYYY-MM-DD HH:MM:SS", type=openapi.TYPE_STRING, required=True
)

@swagger_auto_schema(
    method='post',
    manual_parameters=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the user'),
            'civil_id': openapi.Schema(type=openapi.TYPE_STRING, description='Civil ID of the user'),
            'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start time in format YYYY-MM-DD HH:MM:SS'),
        },
        required=['name', 'civil_id', 'start_time'],
    ),
    responses={200: "Booking created successfully", 400: "Error message"}
)
@api_view(['POST'])
def create_booking(request):
    if request.method == 'POST':
        try:
            # Parse JSON input
            data = json.loads(request.body)
            name = data.get('name')
            civil_id = data.get('civil_id')
            start_time_str = data.get('start_time')

            # Validate inputs
            if not name or not civil_id or not start_time_str:
                return JsonResponse({'error': 'All fields (name, civil_id, start_time) are required.'}, status=400)

            try:
                # Parse start_time
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return JsonResponse({'error': 'Invalid start_time format. Use YYYY-MM-DD HH:MM:SS.'}, status=400)

            # Calculate end_time
            duration_minutes = settings.BOOKING_DURATION
            end_time = start_time + timedelta(minutes=duration_minutes)

            # Check for overlapping bookings
            overlapping_booking = Booking.objects.filter(
                start_time__lt=end_time,
                start_time__gte=start_time
            ).exists()

            if overlapping_booking:
                return JsonResponse({'error': 'A booking already exists for the selected time slot.'}, status=400)

            # Create Booking
            booking = Booking(name=name, civil_id=civil_id, start_time=start_time)

            # Generate QR Code
            qr_data = f"Booking for {name} ({civil_id}) from {start_time} to {end_time}"
            qr = qrcode.make(qr_data)
            qr_io = io.BytesIO()
            qr.save(qr_io, format='PNG')
            booking.qr_code.save(f"qr_{name}.png", ContentFile(qr_io.getvalue()), save=False)

            booking.save()

            return JsonResponse({
                'message': 'Booking created successfully',
                'booking_id': booking.id,
                'start_time': booking.start_time,
                'end_time': booking.end_time()  # Call the dynamic method
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON input.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="List of all bookings"
        ),
        400: "Invalid request method"
    }
)
@api_view(['GET'])
def get_all_bookings(request):
    if request.method == 'GET':
        # Retrieve all bookings
        bookings = Booking.objects.all()

        # Serialize the data
        booking_list = [
            {
                "id": booking.id,
                "name": booking.name,
                "civil_id": booking.civil_id,
                "start_time": booking.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": (booking.start_time + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S"),
                "qr_code_url": booking.qr_code.url if booking.qr_code else None
            }
            for booking in bookings
        ]

        return JsonResponse({"bookings": booking_list}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
