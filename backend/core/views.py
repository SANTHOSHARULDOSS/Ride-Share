import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse, HttpResponseForbidden
from django.core.management import call_command
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import User, Vehicle, Ride, RouteWaypoint, Booking
from .forms import UserProfileForm, VehicleForm, RidePublishForm
from .route_matching import match_rides_for_passenger

User = get_user_model()

# ---------------------------------------------------------------------
# Landing & Authentication
# ---------------------------------------------------------------------
def landing_view(request):
    """Render landing page with general information."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def login_view(request):
    """
    Standard login view with a special 'demo_role' helper
    for instant authentication of mock users during demonstrations.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    demo_role = request.GET.get('demo_role')
    if demo_role:
        username = None
        password = None
        if demo_role == 'ADMIN':
            username, password = 'admin', 'admin123'
        elif demo_role == 'DRIVER':
            username, password = 'driver', 'driver123'
        elif demo_role == 'PASSENGER':
            username, password = 'passenger', 'pass123'

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Logged in as demo {demo_role.lower()} successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, f"Unable to authenticate demo user: {username}.")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('landing')

# ---------------------------------------------------------------------
# Dashboard & Role Redirection
# ---------------------------------------------------------------------
@login_required
def dashboard_view(request):
    """Redirect to the appropriate dashboard based on user role."""
    if request.user.role == 'ADMIN':
        return redirect('dashboard_admin')
    elif request.user.role == 'DRIVER':
        return redirect('dashboard_driver')
    else:
        return redirect('dashboard_passenger')

@login_required
def dashboard_passenger(request):
    if request.user.role != 'PASSENGER':
        return redirect('dashboard')

    # Get bookings stats
    bookings = Booking.objects.filter(passenger=request.user).select_related('ride', 'ride__driver')
    total_bookings = bookings.count()
    active_bookings = bookings.filter(status__in=[Booking.Status.PENDING, Booking.Status.ACCEPTED]).count()
    completed_bookings = bookings.filter(status=Booking.Status.COMPLETED).count()
    total_spend = bookings.filter(status=Booking.Status.COMPLETED).aggregate(Sum('total_price'))['total_price__sum'] or 0.00

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'total_spend': total_spend,
    }
    return render(request, 'dashboard_passenger.html', context)

@login_required
def dashboard_driver(request):
    if request.user.role != 'DRIVER':
        return redirect('dashboard')

    vehicle = Vehicle.objects.filter(driver=request.user).first()
    rides = Ride.objects.filter(driver=request.user).order_by('-departure_time')
    
    total_rides = rides.count()
    active_rides = rides.filter(status=Ride.Status.ACTIVE).count()
    completed_rides = rides.filter(status=Ride.Status.COMPLETED).count()
    
    # Calculate earnings from completed bookings on driver's rides
    total_earnings = Booking.objects.filter(
        ride__driver=request.user, 
        status=Booking.Status.COMPLETED
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0.00

    # Pending ride bookings waiting for approval
    pending_bookings = Booking.objects.filter(
        ride__driver=request.user,
        status=Booking.Status.PENDING
    ).select_related('ride', 'passenger')

    context = {
        'vehicle': vehicle,
        'rides': rides,
        'total_rides': total_rides,
        'active_rides': active_rides,
        'completed_rides': completed_rides,
        'total_earnings': total_earnings,
        'pending_bookings': pending_bookings,
    }
    return render(request, 'dashboard_driver.html', context)

@login_required
def dashboard_admin(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')

    users_count = User.objects.count()
    drivers_count = User.objects.filter(role='DRIVER').count()
    passengers_count = User.objects.filter(role='PASSENGER').count()
    
    rides_count = Ride.objects.count()
    active_rides_count = Ride.objects.filter(status=Ride.Status.ACTIVE).count()
    bookings_count = Booking.objects.count()
    completed_bookings_count = Booking.objects.filter(status=Booking.Status.COMPLETED).count()

    total_revenue = Booking.objects.filter(status=Booking.Status.COMPLETED).aggregate(Sum('total_price'))['total_price__sum'] or 0.00
    
    recent_rides = Ride.objects.all().order_by('-created_at')[:5].select_related('driver')
    recent_users = User.objects.all().order_by('-date_joined')[:5]

    context = {
        'users_count': users_count,
        'drivers_count': drivers_count,
        'passengers_count': passengers_count,
        'rides_count': rides_count,
        'active_rides_count': active_rides_count,
        'bookings_count': bookings_count,
        'completed_bookings_count': completed_bookings_count,
        'total_revenue': total_revenue,
        'recent_rides': recent_rides,
        'recent_users': recent_users,
    }
    return render(request, 'dashboard_admin.html', context)

# ---------------------------------------------------------------------
# Profile & Vehicle Management
# ---------------------------------------------------------------------
@login_required
def profile_view(request):
    """View and update profile + Vehicle details if user is a driver."""
    user = request.user
    vehicle = None
    vehicle_form = None

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
        
        if user.role == 'DRIVER':
            vehicle = Vehicle.objects.filter(driver=user).first()
            vehicle_form = VehicleForm(request.POST, instance=vehicle)
            
            if profile_form.is_valid() and vehicle_form.is_valid():
                profile_form.save()
                v_instance = vehicle_form.save(commit=False)
                v_instance.driver = user
                v_instance.save()
                messages.success(request, "Profile and vehicle updated successfully!")
                return redirect('profile')
        else:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)
        if user.role == 'DRIVER':
            vehicle = Vehicle.objects.filter(driver=user).first()
            vehicle_form = VehicleForm(instance=vehicle)

    context = {
        'profile_form': profile_form,
        'vehicle_form': vehicle_form,
        'vehicle': vehicle,
    }
    return render(request, 'profile.html', context)

# ---------------------------------------------------------------------
# Ride Searches & Route Waypoint Matching
# ---------------------------------------------------------------------
@login_required
def ride_search_view(request):
    """
    Search rides with intelligent route matching.
    Input parameters:
      - pickup_lat, pickup_lng
      - dropoff_lat, dropoff_lng
      - pickup_name, dropoff_name
      - seats_needed
    """
    matches = []
    searched = False
    
    # Get request parameters
    pickup_name = request.GET.get('pickup_name', '')
    dropoff_name = request.GET.get('dropoff_name', '')
    seats_needed = int(request.GET.get('seats', 1))
    
    pickup_lat = request.GET.get('pickup_lat')
    pickup_lng = request.GET.get('pickup_lng')
    dropoff_lat = request.GET.get('dropoff_lat')
    dropoff_lng = request.GET.get('dropoff_lng')

    if pickup_lat and pickup_lng and dropoff_lat and dropoff_lng:
        searched = True
        matches = match_rides_for_passenger(
            pickup_lat=float(pickup_lat),
            pickup_lng=float(pickup_lng),
            dropoff_lat=float(dropoff_lat),
            dropoff_lng=float(dropoff_lng),
            seats_needed=seats_needed
        )

    # Fetch active rides for smart client-side waypoint matching
    active_rides = Ride.objects.filter(
        status=Ride.Status.ACTIVE,
        departure_time__gte=timezone.now()
    ).select_related('driver', 'vehicle').prefetch_related('waypoints')

    active_rides_list = []
    for ride in active_rides:
        active_rides_list.append({
            'id': ride.id,
            'driver': ride.driver.username,
            'vehicle': f"{ride.vehicle.make} {ride.vehicle.model} ({ride.vehicle.license_plate})",
            'price_per_seat': float(ride.price_per_seat),
            'available_seats': ride.available_seats,
            'departure_time': ride.departure_time.isoformat() if ride.departure_time else "",
            'waypoints': [{
                'name': wp.name,
                'lat': float(wp.latitude),
                'lng': float(wp.longitude),
                'seq': wp.sequence_order
            } for wp in ride.waypoints.all().order_by('sequence_order')]
        })

    context = {
        'pickup_name': pickup_name,
        'dropoff_name': dropoff_name,
        'seats_needed': seats_needed,
        'pickup_lat': pickup_lat,
        'pickup_lng': pickup_lng,
        'dropoff_lat': dropoff_lat,
        'dropoff_lng': dropoff_lng,
        'matches': matches,
        'searched': searched,
        'active_rides_json': json.dumps(active_rides_list),
    }
    return render(request, 'ride_search.html', context)

# ---------------------------------------------------------------------
# Ride Publishing
# ---------------------------------------------------------------------
@login_required
def ride_publish_view(request):
    """
    Drivers publish rides.
    Supports inputting waypoints coordinates and names via an interactive Leaflet map interface
    posted as a JSON waypoint payload.
    """
    if request.user.role != 'DRIVER':
        messages.error(request, "Only drivers can publish rides.")
        return redirect('dashboard')

    vehicle = Vehicle.objects.filter(driver=request.user).first()
    if not vehicle:
        messages.warning(request, "Please register your vehicle in your profile before publishing a ride.")
        return redirect('profile')

    if request.method == 'POST':
        form = RidePublishForm(request.POST, driver=request.user)
        waypoints_json = request.POST.get('waypoints_json', '[]')
        
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.status = Ride.Status.ACTIVE
            ride.save()

            # Parse Waypoints
            try:
                waypoints_data = json.loads(waypoints_json)
                for idx, wp in enumerate(waypoints_data):
                    RouteWaypoint.objects.create(
                        ride=ride,
                        sequence_order=idx,
                        name=wp.get('name', f"Waypoint {idx}"),
                        latitude=wp.get('lat'),
                        longitude=wp.get('lng'),
                        estimated_arrival=ride.departure_time  # Simple simulation offset
                    )
                messages.success(request, "Ride published successfully with waypoints!")
                return redirect('dashboard_driver')
            except Exception as e:
                ride.delete()
                messages.error(request, f"Error processing route waypoints: {str(e)}")
    else:
        form = RidePublishForm(driver=request.user)

    return render(request, 'ride_publish.html', {'form': form, 'vehicle': vehicle})

# ---------------------------------------------------------------------
# Ride Details & Booking Lifecycle
# ---------------------------------------------------------------------
@login_required
def ride_details_view(request, pk):
    ride = get_object_or_404(Ride.objects.select_related('driver', 'vehicle'), pk=pk)
    waypoints = ride.waypoints.all().order_by('sequence_order')
    
    # Check if passenger has already booked
    existing_booking = None
    if request.user.role == 'PASSENGER':
        existing_booking = Booking.objects.filter(ride=ride, passenger=request.user).first()

    # Get active passengers for driver
    bookings = []
    if request.user == ride.driver or request.user.role == 'ADMIN':
        bookings = Booking.objects.filter(ride=ride).select_related('passenger')

    # Convert waypoints to JSON for map rendering
    waypoints_list = []
    for wp in waypoints:
        waypoints_list.append({
            'name': wp.name,
            'lat': float(wp.latitude),
            'lng': float(wp.longitude),
            'sequence': wp.sequence_order
        })

    context = {
        'ride': ride,
        'waypoints': waypoints,
        'waypoints_json': json.dumps(waypoints_list),
        'existing_booking': existing_booking,
        'bookings': bookings,
    }
    return render(request, 'ride_details.html', context)

@login_required
def booking_create_view(request, ride_id):
    """Passengers request a booking and get redirected to the payment simulation."""
    if request.user.role != 'PASSENGER':
        return HttpResponseForbidden("Only passengers can book rides.")
        
    ride = get_object_or_404(Ride, pk=ride_id)
    
    if request.method == 'POST':
        seats_requested = int(request.POST.get('seats_requested', 1))
        pickup_location = request.POST.get('pickup_name', ride.start_location)
        pickup_lat = float(request.POST.get('pickup_lat', 0.0))
        pickup_lng = float(request.POST.get('pickup_lng', 0.0))
        dropoff_location = request.POST.get('dropoff_name', ride.end_location)
        dropoff_lat = float(request.POST.get('dropoff_lat', 0.0))
        dropoff_lng = float(request.POST.get('dropoff_lng', 0.0))
        
        if seats_requested > ride.available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('ride_details', pk=ride_id)
            
        total_price = ride.price_per_seat * seats_requested
        
        booking = Booking.objects.create(
            ride=ride,
            passenger=request.user,
            pickup_location=pickup_location,
            pickup_lat=pickup_lat,
            pickup_lng=pickup_lng,
            dropoff_location=dropoff_location,
            dropoff_lat=dropoff_lat,
            dropoff_lng=dropoff_lng,
            seats_requested=seats_requested,
            total_price=total_price,
            status=Booking.Status.PENDING
        )
        
        # Redirect passenger to checkout screen
        return redirect('payment_simulate', booking_id=booking.id)

    return redirect('ride_details', pk=ride_id)

@login_required
def booking_action_view(request, booking_id):
    """Drivers approve or reject bookings."""
    booking = get_object_or_404(Booking.objects.select_related('ride'), pk=booking_id)
    
    if request.user != booking.ride.driver:
        return HttpResponseForbidden("Not authorized to manage this booking.")

    action = request.POST.get('action')
    if action == 'accept':
        if booking.seats_requested <= booking.ride.available_seats:
            booking.status = Booking.Status.ACCEPTED
            booking.ride.available_seats -= booking.seats_requested
            booking.ride.save()
            booking.save()
            messages.success(request, f"Booking for {booking.passenger.username} accepted!")
        else:
            messages.error(request, "Not enough available seats left on this ride.")
    elif action == 'reject':
        booking.status = Booking.Status.REJECTED
        booking.save()
        messages.warning(request, f"Booking for {booking.passenger.username} rejected.")

    return redirect('dashboard')

@login_required
def ride_status_update_view(request, pk):
    """Drivers update ride status (Active, Completed, Cancelled)."""
    ride = get_object_or_404(Ride, pk=pk)
    
    if request.user != ride.driver:
        return HttpResponseForbidden("Not authorized.")

    new_status = request.POST.get('status')
    if new_status in Ride.Status.values:
        ride.status = new_status
        ride.save()
        
        # Complete all bookings if ride is completed
        if new_status == Ride.Status.COMPLETED:
            Booking.objects.filter(ride=ride, status=Booking.Status.ACCEPTED).update(status=Booking.Status.COMPLETED)
            messages.success(request, "Ride completed! Bookings marked completed.")
        elif new_status == Ride.Status.CANCELLED:
            # Restore seats & cancel bookings
            bookings = Booking.objects.filter(ride=ride, status=Booking.Status.ACCEPTED)
            for b in bookings:
                ride.available_seats += b.seats_requested
            ride.save()
            Booking.objects.filter(ride=ride).update(status=Booking.Status.CANCELLED)
            messages.warning(request, "Ride cancelled. Bookings cancelled.")
        else:
            messages.success(request, f"Ride status updated to {ride.get_status_display()}.")

    return redirect('ride_details', pk=pk)

# ---------------------------------------------------------------------
# Payment Simulation Screen
# ---------------------------------------------------------------------
@login_required
def payment_simulate_view(request, booking_id):
    booking = get_object_or_404(Booking.objects.select_related('ride', 'passenger'), pk=booking_id)
    
    if request.user != booking.passenger:
        return HttpResponseForbidden("Not authorized.")

    if request.method == 'POST':
        payment_status = request.POST.get('payment_status') # SUCCESS, FAILURE, PENDING
        
        if payment_status == 'SUCCESS':
            # Payment completed successfully. Wait for driver approval or update status
            messages.success(request, "Payment successful! Your booking is pending driver approval.")
            return redirect('dashboard')
        elif payment_status == 'PENDING':
            messages.info(request, "Payment processing. Booking request submitted.")
            return redirect('dashboard')
        else:
            booking.status = Booking.Status.CANCELLED
            booking.save()
            messages.error(request, "Payment failed. Booking has been cancelled.")
            return redirect('dashboard')

    return render(request, 'payment.html', {'booking': booking})

# ---------------------------------------------------------------------
# Database Reseeding for Administrators
# ---------------------------------------------------------------------
@login_required
def admin_reset_view(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Only administrators can perform database reset.")

    try:
        call_command('seed_demo')
        messages.success(request, "Database seeded and reset to default successfully!")
    except Exception as e:
        messages.error(request, f"Error resetting database: {str(e)}")

    return redirect('dashboard')

# ---------------------------------------------------------------------
# Offline Fallback View
# ---------------------------------------------------------------------
def offline_view(request):
    return render(request, 'offline.html')

# ---------------------------------------------------------------------
# Dynamic Project Report View
# ---------------------------------------------------------------------
@login_required
def project_report_view(request):
    """
    Renders the PROJECT_REPORT.md file dynamically on the web interface.
    """
    import os
    from django.conf import settings
    
    report_path = os.path.join(settings.BASE_DIR, '..', 'docs', '09_Project_Report', 'PROJECT_REPORT.md')
    content = ""
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# Project Report\n\nReport file not found locally."
        
    return render(request, 'project_report.html', {'report_content': content})

