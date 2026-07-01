import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, Vehicle, Ride, RouteWaypoint, Booking

class Command(BaseCommand):
    help = 'Seeds the database with demo users, vehicles, and rides'

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing data...")
        Booking.objects.all().delete()
        RouteWaypoint.objects.all().delete()
        Ride.objects.all().delete()
        Vehicle.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating demo users...")
        
        # 1. Administrator
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@rideshare.local',
            password='admin123',
            role='ADMIN',
            phone_number='+919999999999'
        )
        self.stdout.write("Admin user created (username: admin, password: admin123)")

        # 2. Driver
        driver = User.objects.create_user(
            username='driver',
            email='driver@rideshare.local',
            password='driver123',
            role='DRIVER',
            phone_number='+919876543210'
        )
        self.stdout.write("Driver user created (username: driver, password: driver123)")

        # 3. Passenger
        passenger = User.objects.create_user(
            username='passenger',
            email='passenger@rideshare.local',
            password='pass123',
            role='PASSENGER',
            phone_number='+919812345678'
        )
        self.stdout.write("Passenger user created (username: passenger, password: pass123)")

        # Additional passenger for booking demo
        passenger2 = User.objects.create_user(
            username='passenger2',
            email='passenger2@rideshare.local',
            password='pass123',
            role='PASSENGER',
            phone_number='+919811122233'
        )

        self.stdout.write("Creating driver vehicle...")
        vehicle = Vehicle.objects.create(
            driver=driver,
            make="Toyota",
            model="Corolla",
            license_plate="DL-3C-AB-1234",
            capacity=4,
            color="Silver"
        )
        self.stdout.write("Vehicle registered for driver.")

        self.stdout.write("Creating demo rides...")
        
        # Ride 1: Delhi Route (Active)
        departure_time1 = timezone.now() + datetime.timedelta(hours=2)
        ride1 = Ride.objects.create(
            driver=driver,
            vehicle=vehicle,
            start_location="New Delhi Railway Station",
            end_location="Indira Gandhi International Airport (T3)",
            departure_time=departure_time1,
            price_per_seat=250.00,
            available_seats=3,
            status=Ride.Status.ACTIVE
        )
        
        # Waypoints for Ride 1
        w1_1 = RouteWaypoint.objects.create(
            ride=ride1,
            sequence_order=0,
            name="New Delhi Railway Station",
            latitude=28.643000,
            longitude=77.222300,
            estimated_arrival=departure_time1
        )
        w1_2 = RouteWaypoint.objects.create(
            ride=ride1,
            sequence_order=1,
            name="Connaught Place",
            latitude=28.630400,
            longitude=77.217700,
            estimated_arrival=departure_time1 + datetime.timedelta(minutes=15)
        )
        w1_3 = RouteWaypoint.objects.create(
            ride=ride1,
            sequence_order=2,
            name="Dhaula Kuan",
            latitude=28.591800,
            longitude=77.161600,
            estimated_arrival=departure_time1 + datetime.timedelta(minutes=35)
        )
        w1_4 = RouteWaypoint.objects.create(
            ride=ride1,
            sequence_order=3,
            name="Indira Gandhi International Airport (T3)",
            latitude=28.556200,
            longitude=77.100000,
            estimated_arrival=departure_time1 + datetime.timedelta(minutes=55)
        )

        # Ride 2: Bangalore Route (Active)
        departure_time2 = timezone.now() + datetime.timedelta(hours=5)
        ride2 = Ride.objects.create(
            driver=driver,
            vehicle=vehicle,
            start_location="Indiranagar Metro Station",
            end_location="Electronic City Phase 1",
            departure_time=departure_time2,
            price_per_seat=120.00,
            available_seats=4,
            status=Ride.Status.ACTIVE
        )

        # Waypoints for Ride 2
        w2_1 = RouteWaypoint.objects.create(
            ride=ride2,
            sequence_order=0,
            name="Indiranagar Metro Station",
            latitude=12.971900,
            longitude=77.641200,
            estimated_arrival=departure_time2
        )
        w2_2 = RouteWaypoint.objects.create(
            ride=ride2,
            sequence_order=1,
            name="Koramangala 5th Block",
            latitude=12.935200,
            longitude=77.624400,
            estimated_arrival=departure_time2 + datetime.timedelta(minutes=25)
        )
        w2_3 = RouteWaypoint.objects.create(
            ride=ride2,
            sequence_order=2,
            name="HSR Layout Sector 1",
            latitude=12.912800,
            longitude=77.638700,
            estimated_arrival=departure_time2 + datetime.timedelta(minutes=45)
        )
        w2_4 = RouteWaypoint.objects.create(
            ride=ride2,
            sequence_order=3,
            name="Electronic City Phase 1",
            latitude=12.839900,
            longitude=77.677000,
            estimated_arrival=departure_time2 + datetime.timedelta(minutes=70)
        )

        # Ride 3: Chennai Central to Sholinganallur (Active)
        departure_time3 = timezone.now() + datetime.timedelta(hours=3)
        ride3 = Ride.objects.create(
            driver=driver,
            vehicle=vehicle,
            start_location="Chennai Central Railway Station",
            end_location="Sholinganallur Junction (OMR)",
            departure_time=departure_time3,
            price_per_seat=150.00,
            available_seats=3,
            status=Ride.Status.ACTIVE
        )
        
        # Waypoints for Ride 3
        RouteWaypoint.objects.create(
            ride=ride3, sequence_order=0, name="Chennai Central Railway Station",
            latitude=13.082700, longitude=80.270700, estimated_arrival=departure_time3
        )
        RouteWaypoint.objects.create(
            ride=ride3, sequence_order=1, name="T. Nagar Bus Terminus",
            latitude=13.040500, longitude=80.233700, estimated_arrival=departure_time3 + datetime.timedelta(minutes=20)
        )
        RouteWaypoint.objects.create(
            ride=ride3, sequence_order=2, name="Guindy Kathipara Junction",
            latitude=13.010100, longitude=80.201500, estimated_arrival=departure_time3 + datetime.timedelta(minutes=40)
        )
        RouteWaypoint.objects.create(
            ride=ride3, sequence_order=3, name="Sholinganallur Junction (OMR)",
            latitude=12.901000, longitude=80.227900, estimated_arrival=departure_time3 + datetime.timedelta(minutes=70)
        )

        # Ride 4: Chennai Airport to Siruseri IT Park (Active)
        departure_time4 = timezone.now() + datetime.timedelta(hours=6)
        ride4 = Ride.objects.create(
            driver=driver,
            vehicle=vehicle,
            start_location="Chennai International Airport",
            end_location="Siruseri SIPCOT IT Park",
            departure_time=departure_time4,
            price_per_seat=180.00,
            available_seats=4,
            status=Ride.Status.ACTIVE
        )
        
        # Waypoints for Ride 4
        RouteWaypoint.objects.create(
            ride=ride4, sequence_order=0, name="Chennai International Airport",
            latitude=12.981600, longitude=80.163800, estimated_arrival=departure_time4
        )
        RouteWaypoint.objects.create(
            ride=ride4, sequence_order=1, name="Velachery Phoenix Marketcity",
            latitude=12.979000, longitude=80.219000, estimated_arrival=departure_time4 + datetime.timedelta(minutes=25)
        )
        RouteWaypoint.objects.create(
            ride=ride4, sequence_order=2, name="Adyar Depot",
            latitude=13.006300, longitude=80.257400, estimated_arrival=departure_time4 + datetime.timedelta(minutes=45)
        )
        RouteWaypoint.objects.create(
            ride=ride4, sequence_order=3, name="Siruseri SIPCOT IT Park",
            latitude=12.827700, longitude=80.218500, estimated_arrival=departure_time4 + datetime.timedelta(minutes=75)
        )

        # Ride 5: Tambaram to Marina Beach (Active)
        departure_time5 = timezone.now() + datetime.timedelta(hours=2)
        ride5 = Ride.objects.create(
            driver=driver,
            vehicle=vehicle,
            start_location="Tambaram Railway Station",
            end_location="Marina Beach Lighthouse",
            departure_time=departure_time5,
            price_per_seat=100.00,
            available_seats=4,
            status=Ride.Status.ACTIVE
        )
        
        # Waypoints for Ride 5
        RouteWaypoint.objects.create(
            ride=ride5, sequence_order=0, name="Tambaram Railway Station",
            latitude=12.922900, longitude=80.127500, estimated_arrival=departure_time5
        )
        RouteWaypoint.objects.create(
            ride=ride5, sequence_order=1, name="Guindy Kathipara Junction",
            latitude=13.010100, longitude=80.201500, estimated_arrival=departure_time5 + datetime.timedelta(minutes=30)
        )
        RouteWaypoint.objects.create(
            ride=ride5, sequence_order=2, name="T. Nagar Bus Terminus",
            latitude=13.040500, longitude=80.233700, estimated_arrival=departure_time5 + datetime.timedelta(minutes=50)
        )
        RouteWaypoint.objects.create(
            ride=ride5, sequence_order=3, name="Marina Beach Lighthouse",
            latitude=13.050000, longitude=80.282400, estimated_arrival=departure_time5 + datetime.timedelta(minutes=75)
        )

        self.stdout.write("Creating demo bookings...")
        # Create a booking from passenger2 on Ride 1 (Connaught Place to Dhaula Kuan)
        booking1 = Booking.objects.create(
            ride=ride1,
            passenger=passenger2,
            pickup_location="Connaught Place",
            pickup_lat=28.630400,
            pickup_lng=77.217700,
            dropoff_location="Dhaula Kuan",
            dropoff_lat=28.591800,
            dropoff_lng=77.161600,
            seats_requested=1,
            total_price=250.00,
            status=Booking.Status.PENDING
        )
        
        # Create a completed booking from passenger on Ride 2
        booking2 = Booking.objects.create(
            ride=ride2,
            passenger=passenger,
            pickup_location="Indiranagar Metro Station",
            pickup_lat=12.971900,
            pickup_lng=77.641200,
            dropoff_location="Koramangala 5th Block",
            dropoff_lat=12.935200,
            dropoff_lng=77.624400,
            seats_requested=2,
            total_price=240.00,
            status=Booking.Status.ACCEPTED
        )

        # Create a pending booking on Chennai Ride 3 (Tambaram to T. Nagar)
        booking3 = Booking.objects.create(
            ride=ride5,
            passenger=passenger2,
            pickup_location="Tambaram Railway Station",
            pickup_lat=12.922900,
            pickup_lng=80.127500,
            dropoff_location="T. Nagar Bus Terminus",
            dropoff_lat=13.040500,
            dropoff_lng=80.233700,
            seats_requested=2,
            total_price=200.00,
            status=Booking.Status.PENDING
        )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
