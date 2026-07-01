import math
from decimal import Decimal
from django.utils import timezone
from .models import Ride, RouteWaypoint

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface
    using the Haversine formula. Returns distance in kilometers.
    """
    # Convert lat/lng to float if they are Decimal
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    R = 6371.0  # Earth radius in kilometers

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

def match_rides_for_passenger(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, seats_needed=1, max_walk_distance_km=5.0):
    """
    Intelligent route matching algorithm:
    1. Finds active rides with enough available seats.
    2. Retrieves sequential waypoints for each ride.
    3. Finds the closest waypoint to the passenger's pickup (index i).
    4. Finds the closest waypoint to the passenger's dropoff (index j).
    5. Checks if pickup is before dropoff (i < j).
    6. Ensures walk/detour distances to pickup and dropoff are within max_walk_distance_km.
    7. Computes a match score and returns matching rides sorted by score.
    """
    active_rides = Ride.objects.filter(
        status=Ride.Status.ACTIVE,
        available_seats__gte=seats_needed,
        departure_time__gte=timezone.now()
    ).select_related('driver', 'vehicle')

    matches = []

    for ride in active_rides:
        waypoints = list(ride.waypoints.all().order_by('sequence_order'))
        if not waypoints:
            continue

        closest_pickup_wp = None
        closest_pickup_idx = -1
        min_pickup_dist = float('inf')

        closest_dropoff_wp = None
        closest_dropoff_idx = -1
        min_dropoff_dist = float('inf')

        # Find closest waypoints
        for idx, wp in enumerate(waypoints):
            pickup_dist = haversine_distance(pickup_lat, pickup_lng, wp.latitude, wp.longitude)
            if pickup_dist < min_pickup_dist:
                min_pickup_dist = pickup_dist
                closest_pickup_wp = wp
                closest_pickup_idx = idx

            dropoff_dist = haversine_distance(dropoff_lat, dropoff_lng, wp.latitude, wp.longitude)
            if dropoff_dist < min_dropoff_dist:
                min_dropoff_dist = dropoff_dist
                closest_dropoff_wp = wp
                closest_dropoff_idx = idx

        # Match Conditions:
        # 1. Pickup waypoint must precede Dropoff waypoint in the driver's route sequence.
        # 2. Both pickup and dropoff distances must be within the acceptable detour threshold.
        if (closest_pickup_idx != -1 and 
            closest_dropoff_idx != -1 and 
            closest_pickup_idx < closest_dropoff_idx and
            min_pickup_dist <= max_walk_distance_km and
            min_dropoff_dist <= max_walk_distance_km):
            
            # Calculate match quality score (0 to 100)
            # A score of 100 means 0 detour/walk distance.
            # Deduct 10 points per km of detour.
            total_walk_dist = min_pickup_dist + min_dropoff_dist
            score = max(0.0, 100.0 - (total_walk_dist * 10.0))

            matches.append({
                'ride': ride,
                'pickup_waypoint': closest_pickup_wp,
                'dropoff_waypoint': closest_dropoff_wp,
                'pickup_distance': round(min_pickup_dist, 2),
                'dropoff_distance': round(min_dropoff_dist, 2),
                'total_walk_distance': round(total_walk_dist, 2),
                'score': round(score, 1),
            })

    # Sort matches by score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches
