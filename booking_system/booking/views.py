import json
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
import io
import qrcode
from django.core.files.base import ContentFile
from booking.models import Booking
from reportlab.pdfgen import canvas

# Importing necessary modules and settings
from django.conf import settings

from booking.serializers import BookingSerializer

# Swagger parameter definitions for documentation
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
            'civil_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Civil ID of the user'),
            'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start time in format YYYY-MM-DD HH:MM'),
        },
        required=['name', 'civil_id', 'start_time'],
    ),
    responses={200: "Booking created successfully", 400: "Error message"}
)
@api_view(['POST'])
def create_booking(request):
    """
    Handles POST requests to create a new booking.
    Validates booking data, checks for overlapping time slots,
    saves the booking, and generates a QR code.
    """
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Calculate booking duration and check for time slot conflicts
            duration_minutes = settings.BOOKING_DURATION
            start_time = serializer.validated_data['start_time']
            end_time = start_time + timedelta(minutes=duration_minutes)

            overlapping_booking = Booking.objects.filter(
                start_time__lt=end_time, start_time__gte=start_time
            ).exists()

            if overlapping_booking:
                # Return error if there is a conflict with an existing booking
                return JsonResponse({'error': 'A booking already exists for the selected time slot.'}, status=400)

            # Save the booking and generate a QR code for it
            booking = serializer.save()
            qr_data = f"Booking for '{booking.name}' from {start_time} to {end_time}"
            qr = qrcode.make(qr_data)
            qr_io = io.BytesIO()
            qr.save(qr_io, format='PNG')
            booking.qr_code.save(f"qr_{booking.name}.png", ContentFile(qr_io.getvalue()), save=False)
            booking.save()

            # Return a success response with the booking details
            response_data = {
                'message': 'Booking created successfully',
                'booking': BookingSerializer(booking).data
            }
            return JsonResponse(response_data, status=200)

        # Return validation errors if any
        return JsonResponse(serializer.errors, status=400)


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
    """
    Handles GET requests to retrieve all bookings.
    Serializes and returns the booking data.
    """
    if request.method == 'GET':
        # Fetch all bookings from the database
        bookings = Booking.objects.all()

        # Serialize the booking data
        serializer = BookingSerializer(bookings, many=True)

        # Return serialized data as a JSON response
        return JsonResponse({"bookings": serializer.data}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('booking_id', openapi.IN_QUERY, description="ID of the booking", type=openapi.TYPE_INTEGER)
    ],
    responses={200: "PDF generated successfully", 400: "Invalid request"}
)
@api_view(['GET'])
def generate_booking_pdf(request):
    """
    Handles GET requests to generate a PDF ticket for a specific booking.
    The PDF includes booking details and the QR code (if available).
    """
    booking_id = request.GET.get('booking_id')

    if not booking_id:
        # Return error if booking ID is missing
        return JsonResponse({'error': 'Booking ID is required.'}, status=400)

    try:
        # Retrieve the booking from the database
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        # Return error if booking is not found
        return JsonResponse({'error': 'Booking not found.'}, status=404)

    # Generate the PDF with booking details
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Add text information to the PDF
    p.drawString(100, 800, f"Booking Ticket")
    p.drawString(100, 780, f"Name: {booking.name}")
    p.drawString(100, 760, f"Civil ID: {booking.civil_id}")
    p.drawString(100, 740, f"Start Time: {booking.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, 720, f"End Time: {(booking.start_time + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')}")

    # Attempt to add the QR code image to the PDF
    try:
        if booking.qr_code:
            qr_code_path = booking.qr_code.path
            p.drawImage(qr_code_path, 100, 600, width=100, height=100)
    except Exception as e:
        # Log error if QR code image cannot be added
        print(f"Error drawing QR Code: {e}")

    # Finalize and save the PDF
    p.showPage()
    p.save()

    # Return the PDF as a response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Booking_{booking_id}.pdf"'
    buffer.close()
    return response
