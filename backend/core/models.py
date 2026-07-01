from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ---------------------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------------------
class User(AbstractUser):
    """Extended user model with role distinction and extra profile info."""
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('DRIVER', 'Driver'),
        ('PASSENGER', 'Passenger'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PASSENGER')
    phone_number = models.CharField(max_length=20, blank=True, help_text='Contact number')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ---------------------------------------------------------------------
# Vehicle Model
# ---------------------------------------------------------------------
class Vehicle(models.Model):
    driver = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(help_text='Total seats available')
    color = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ['driver__username']

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

# ---------------------------------------------------------------------
# Ride Model
# ---------------------------------------------------------------------
class Ride(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    driver = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='rides')
    vehicle = models.ForeignKey('core.Vehicle', on_delete=models.PROTECT, related_name='rides')
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ride'
        verbose_name_plural = 'Rides'
        ordering = ['-departure_time']

    def __str__(self):
        return f"Ride {self.id} by {self.driver.username}"

# ---------------------------------------------------------------------
# RouteWaypoint Model
# ---------------------------------------------------------------------
class RouteWaypoint(models.Model):
    ride = models.ForeignKey('core.Ride', on_delete=models.CASCADE, related_name='waypoints')
    sequence_order = models.PositiveIntegerField(help_text='Order of the waypoint in the route')
    name = models.CharField(max_length=255, help_text='Human readable place name')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    estimated_arrival = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Route Waypoint'
        verbose_name_plural = 'Route Waypoints'
        ordering = ['ride', 'sequence_order']
        unique_together = ('ride', 'sequence_order')

    def __str__(self):
        return f"{self.name} (Ride {self.ride.id} - #{self.sequence_order})"

# ---------------------------------------------------------------------
# Booking Model
# ---------------------------------------------------------------------
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    ride = models.ForeignKey('core.Ride', on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='bookings')
    pickup_location = models.CharField(max_length=255)
    pickup_lat = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_lng = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_location = models.CharField(max_length=255)
    dropoff_lat = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_lng = models.DecimalField(max_digits=9, decimal_places=6)
    seats_requested = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.id} by {self.passenger.username} for Ride {self.ride.id}"
