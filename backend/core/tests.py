import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Vehicle, Ride, RouteWaypoint, Booking
from .route_matching import match_rides_for_passenger, haversine_distance

User = get_user_model()

class RouteMatchingTestCase(TestCase):
    def setUp(self):
        # Create driver
        self.driver = User.objects.create_user(
            username='driver_test',
            email='driver@test.com',
            password='testpassword123',
            role='DRIVER'
        )
        # Create passenger
        self.passenger = User.objects.create_user(
            username='passenger_test',
            email='passenger@test.com',
            password='testpassword123',
            role='PASSENGER'
        )
        # Create vehicle
        self.vehicle = Vehicle.objects.create(
            driver=self.driver,
            make="Honda",
            model="Civic",
            license_plate="MH-12-AB-9999",
            capacity=4,
            color="Red"
        )
        # Create active ride
        self.departure_time = timezone.now() + datetime.timedelta(hours=2)
        self.ride = Ride.objects.create(
            driver=self.driver,
            vehicle=self.vehicle,
            start_location="Start Landmark",
            end_location="End Landmark",
            departure_time=self.departure_time,
            price_per_seat=100.00,
            available_seats=4,
            status=Ride.Status.ACTIVE
        )
        # Add waypoints along a straight-ish path (approximately 11km total)
        # Point A: (12.97, 77.64) - Start
        # Point B: (12.93, 77.62) - Midpoint (approx 5.5km away)
        # Point C: (12.91, 77.60) - End (approx 5.5km further)
        self.wp0 = RouteWaypoint.objects.create(
            ride=self.ride,
            sequence_order=0,
            name="Point A",
            latitude=12.970000,
            longitude=77.640000,
            estimated_arrival=self.departure_time
        )
        self.wp1 = RouteWaypoint.objects.create(
            ride=self.ride,
            sequence_order=1,
            name="Point B",
            latitude=12.930000,
            longitude=77.620000,
            estimated_arrival=self.departure_time + datetime.timedelta(minutes=15)
        )
        self.wp2 = RouteWaypoint.objects.create(
            ride=self.ride,
            sequence_order=2,
            name="Point C",
            latitude=12.910000,
            longitude=77.600000,
            estimated_arrival=self.departure_time + datetime.timedelta(minutes=30)
        )

    def test_haversine_formula(self):
        # Distance between Point A (12.97, 77.64) and Point B (12.93, 77.62)
        # Expected distance is ~4.9km
        dist = haversine_distance(12.97, 77.64, 12.93, 77.62)
        self.assertGreater(dist, 4.0)
        self.assertLess(dist, 6.0)

    def test_successful_route_match(self):
        # Passenger wants to go from Point A to Point B
        # Let's search with slightly offset coordinates
        matches = match_rides_for_passenger(
            passenger=self.passenger,
            pickup_lat=12.969, pickup_lng=77.639,  # Very close to Point A
            dropoff_lat=12.931, dropoff_lng=77.621, # Very close to Point B
            seats_needed=1,
            max_walk_distance_km=2.0
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['ride'], self.ride)
        # Score should be very high (near 100) since distances are minimal
        self.assertGreater(matches[0]['score'], 90.0)

    def test_incorrect_direction_no_match(self):
        # Passenger wants to travel in reverse (Point B to Point A)
        matches = match_rides_for_passenger(
            passenger=self.passenger,
            pickup_lat=12.931, pickup_lng=77.621,
            dropoff_lat=12.969, dropoff_lng=77.639,
            seats_needed=1,
            max_walk_distance_km=2.0
        )
        # Should not match because closest pickup waypoint (wp1) has sequence_order = 1
        # and closest dropoff waypoint (wp0) has sequence_order = 0. (i < j condition fails)
        self.assertEqual(len(matches), 0)

    def test_too_far_no_match(self):
        # Passenger is in a completely different area
        matches = match_rides_for_passenger(
            passenger=self.passenger,
            pickup_lat=13.500000, pickup_lng=78.500000,
            dropoff_lat=12.910000, dropoff_lng=77.600000,
            seats_needed=1,
            max_walk_distance_km=5.0
        )
        self.assertEqual(len(matches), 0)
