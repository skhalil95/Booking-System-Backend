Project Overview
----------------
This is a Django-based project designed to handle bookings. The application provides the following features:
- Create a booking.
- List all bookings.
- Generate a PDF for a booking.
- API documentation using Swagger.

Prerequisites
-------------
To set up and run this project, ensure you have the following installed:
- Python 3.8 or later
- pip (Python package installer)
- Virtual environment (optional but recommended)

Installation
------------
1. Download Dependencies:
   Run the following command to install all required dependencies:
   > pip install -r requirements.txt

2. Apply Migrations:
   Run the following commands to apply database migrations:
   > python manage.py makemigrations
   > python manage.py migrate

3. Run the Application:
   Start the development server by running:
   > python manage.py runserver

   Access the application at:
   http://127.0.0.1:8000/

API Documentation
-----------------
Swagger Documentation:
Access the Swagger documentation at:
http://127.0.0.1:8000/swagger/

Contact
-------
For support, contact:
Email: support@example.com
