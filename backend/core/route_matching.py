import math
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from .models import Ride, RouteWaypoint, Friendship, CommunityMember, EventAttendee

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

def match_rides_for_passenger(passenger, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, seats_needed=1, max_walk_distance_km=5.0):
    """
    Intelligent recommendation engine:
    1. Filters active rides by seats and departure time.
    2. Identifies pickup and dropoff waypoint overlays along the driver's route.
    3. Calculates distance detour scores.
    4. Computes trust and affiliation boosts:
       - Shared College: +15 points
       - Shared Company/Org: +15 points
       - Shared Communities: +10 points
       - Direct Friend status: +10 points
       - Attending Same Event: +10 points
    5. Returns matches ranked by the combined score (0 to 150 scale).
    """
    active_rides = Ride.objects.filter(
        status=Ride.Status.ACTIVE,
        available_seats__gte=seats_needed,
        departure_time__gte=timezone.now()
    ).exclude(driver=passenger).select_related('driver', 'vehicle')

    matches = []

    # Pre-fetch passenger social context to speed up calculations
    passenger_friends = list(Friendship.objects.filter(
        Q(user=passenger, status='ACCEPTED') | Q(friend=passenger, status='ACCEPTED')
    ).values_list('user_id', 'friend_id'))
    
    friend_ids = set()
    for u1, u2 in passenger_friends:
        friend_ids.add(u1 if u1 != passenger.id else u2)

    passenger_comms = set(CommunityMember.objects.filter(
        user=passenger, status='APPROVED'
    ).values_list('community_id', flat=True))

    passenger_events = set(EventAttendee.objects.filter(
        user=passenger, status='GOING'
    ).values_list('event_id', flat=True))

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

        # Find closest sequential waypoints
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

        # Valid sequential overlap criteria
        if (closest_pickup_idx != -1 and 
            closest_dropoff_idx != -1 and 
            closest_pickup_idx < closest_dropoff_idx and
            min_pickup_dist <= max_walk_distance_km and
            min_dropoff_dist <= max_walk_distance_km):
            
            # Base Proximity Score (max 100 points, subtract 10 points per km detour)
            total_detour = min_pickup_dist + min_dropoff_dist
            base_score = max(0.0, 100.0 - (total_detour * 10.0))
            
            # Trust / Affiliation Boosts (max +50 points total)
            boost = 0.0
            driver = ride.driver
            reasons = []

            # 1. College Boost
            if passenger.verified_college and driver.verified_college and passenger.verified_college == driver.verified_college:
                boost += 15.0
                reasons.append(f"🎓 Same College ({passenger.verified_college})")

            # 2. Company/Organization Boost
            if passenger.verified_org and driver.verified_org and passenger.verified_org == driver.verified_org:
                boost += 15.0
                reasons.append(f"💼 Same Company ({passenger.verified_org})")

            # 3. Direct Friend status
            if driver.id in friend_ids:
                boost += 10.0
                reasons.append("👥 Direct Connection (Friend)")

            # 4. Shared Communities
            driver_comms = set(CommunityMember.objects.filter(
                user=driver, status='APPROVED'
            ).values_list('community_id', flat=True))
            shared_comms = passenger_comms.intersection(driver_comms)
            if shared_comms:
                boost += 10.0
                reasons.append(f"🏘️ {len(shared_comms)} Shared Communities")

            # 5. Attending Same Event
            driver_events = set(EventAttendee.objects.filter(
                user=driver, status='GOING'
            ).values_list('event_id', flat=True))
            shared_events = passenger_events.intersection(driver_events)
            if shared_events:
                boost += 10.0
                reasons.append("📅 Attending Same Event")

            final_score = base_score + boost
            # Round values
            matches.append({
                'ride': ride,
                'pickup_waypoint': closest_pickup_wp,
                'dropoff_waypoint': closest_dropoff_wp,
                'pickup_distance': round(min_pickup_dist, 2),
                'dropoff_distance': round(min_dropoff_dist, 2),
                'total_walk_distance': round(total_detour, 2),
                'base_score': round(base_score, 1),
                'boost': round(boost, 1),
                'score': round(final_score, 1),
                'match_reasons': reasons
            })

    # Sort matches by final recommendation score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

