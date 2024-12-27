from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

# Define the schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Slot Booking API",  # Title of the API
        default_version='v1',  # API version
        description="API documentation for the Slot Booking system",  # Brief description of the API
        contact=openapi.Contact(email="sarahmkhalil95@gmail.com"),  # Contact email for API support
    ),
    public=True,  # Allow public access to the schema
    permission_classes=(permissions.AllowAny,),  # Grant unrestricted access to the documentation
)

# Define the main URL patterns
urlpatterns = [
    # Admin site URLs
    path('admin/', admin.site.urls),

    # Include URLs from the 'booking' app under the '/api/' prefix
    path('api/', include('booking.urls')),

    # Swagger UI for API documentation at '/swagger/'
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # ReDoc UI for API documentation at '/redoc/'
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
