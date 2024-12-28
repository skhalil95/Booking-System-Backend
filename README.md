# Reservation Booking System

## Project Overview

This is a Django-based project designed to handle bookings. The application provides the following features:

- Create a booking.
- List all bookings.
- Generate a PDF for a booking.
- API documentation using Swagger and ReDoc.

---

## Prerequisites

To set up and run this project, ensure you have the following installed:

- Python 3.8 or later
- pip (Python package installer)
- Virtual environment (optional but recommended)

---

## Installation

### 1. Navigate to project directory

```bash
cd booking_system
```

### 2. Download Dependencies

To install all required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### 3. Backend URLs Configuration

This configuration allows the backend Django application to accept requests from the specified frontend URL.
Make sure the following environment variables are correctly configured in your .env file located at the root of your project:

```bash
FRONTEND_URL=http://localhost:5173
```

### 4. Apply Migrations

Run the following commands to apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Application

Start the development server by running:

```bash
python manage.py runserver
```

Access the application at:

```
http://127.0.0.1:8000/
```

---

## API Documentation

### Swagger

Access the Swagger documentation at:

```
http://127.0.0.1:8000/swagger/
```

---

---

## Assumptions

1. Reservation Slot Duration: Each reservation slot is fixed at 60 minutes.
2. Slot Availability: Slots are available daily between 9:00 AM and 4:00 PM.
3. Weekly Calendar Scope: The booking system is designed to manage reservations on a weekly basis, focusing on short-term planning rather than long-term or yearly reservations.

---

## Contact

For support, contact:

- Email: [support@example.com](mailto:support@example.com)
