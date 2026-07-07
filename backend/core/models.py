from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ---------------------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------------------
class User(AbstractUser):
    """Extended user model with role distinction, reputation, verification, and profile fields."""
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('DRIVER', 'Driver'),
        ('PASSENGER', 'Passenger'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PASSENGER')
    phone_number = models.CharField(max_length=20, blank=True, help_text='Contact number')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, default='')
    skills = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated skills')
    interests = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated interests')
    languages = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated languages')
    travel_preferences = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated preferences')

    reputation_points = models.IntegerField(default=100)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_gov_id_verified = models.BooleanField(default=False)
    verified_org = models.CharField(max_length=100, blank=True, null=True, help_text='Verified employer')
    verified_college = models.CharField(max_length=100, blank=True, null=True, help_text='Verified college')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ---------------------------------------------------------------------
# User Session (for Login History & Session Management)
# ---------------------------------------------------------------------
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, default='')
    device_type = models.CharField(max_length=50, blank=True, default='Web')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session for {self.user.username} ({self.device_type} - {self.ip_address})"

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
    verified = models.BooleanField(default=False)
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
    
    # Cost sharing, luggage details, emergency contact, and route coordinates map (JSON-like)
    cost_sharing = models.CharField(max_length=100, default='Equal Split')
    luggage_details = models.CharField(max_length=255, blank=True, default='')
    emergency_contact = models.CharField(max_length=100, blank=True, default='')
    route_map = models.TextField(blank=True, default='', help_text='JSON waypoint array path')
    
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

# ---------------------------------------------------------------------
# Community Model
# ---------------------------------------------------------------------
class Community(models.Model):
    TYPE_CHOICES = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    CATEGORY_CHOICES = (
        ('FRIENDS', 'Friends'),
        ('COLLEGE', 'College'),
        ('COMPANY', 'Company'),
        ('OFFICE', 'Office'),
        ('ORGANIZATION', 'Organization'),
        ('EVENT', 'Event'),
        ('FAMILY', 'Family'),
        ('TRAVEL', 'Travel'),
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    banner = models.ImageField(upload_to='community_banners/', blank=True, null=True)
    avatar = models.ImageField(upload_to='community_avatars/', blank=True, null=True)
    rules = models.TextField(blank=True, default='')
    community_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='PUBLIC')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='TRAVEL')
    invite_link = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='communities_created')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'
        ordering = ['name']

    def __str__(self):
        return self.name

class CommunityMember(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MODERATOR', 'Moderator'),
        ('MEMBER', 'Member'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='APPROVED')
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Community Member'
        verbose_name_plural = 'Community Members'
        unique_together = ('community', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.community.name} ({self.role})"

# ---------------------------------------------------------------------
# Friendship Model
# ---------------------------------------------------------------------
class Friendship(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('BLOCKED', 'Blocked'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_initiated')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username} ({self.status})"

# ---------------------------------------------------------------------
# Message (Real-Time Chat) Model
# ---------------------------------------------------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Messaging Context
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')

    content = models.TextField()
    file_attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    file_name = models.CharField(max_length=255, blank=True, default='')
    file_type = models.CharField(max_length=100, blank=True, default='')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']

    def __str__(self):
        return f"Msg {self.id} from {self.sender.username}"

# ---------------------------------------------------------------------
# Notification Model
# ---------------------------------------------------------------------
class Notification(models.Model):
    TYPE_CHOICES = (
        ('FRIEND_REQUEST', 'Friend Request'),
        ('COMMUNITY_INVITE', 'Community Invite'),
        ('TRIP_REQUEST', 'Trip Request'),
        ('TRIP_ACCEPTED', 'Trip Accepted'),
        ('COMMENT', 'Comment'),
        ('LIKE', 'Like'),
        ('MESSAGE', 'Message'),
        ('ADMIN_ANNOUNCEMENT', 'Admin Announcement'),
        ('GENERAL', 'General'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='GENERAL')
    content = models.TextField()
    link = models.CharField(max_length=255, blank=True, default='')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif to {self.recipient.username} ({self.notification_type})"

# ---------------------------------------------------------------------
# Event Planner Model
# ---------------------------------------------------------------------
class Event(models.Model):
    TYPE_CHOICES = (
        ('MEETUP', 'Meetup'),
        ('TOUR', 'Tour'),
        ('OFFICE_TRIP', 'Office Trip'),
        ('COLLEGE_IV', 'College IV'),
        ('HACKATHON', 'Hackathon'),
        ('TREKKING', 'Trekking'),
        ('BIKERIDE', 'Bike Ride'),
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    event_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='MEETUP')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, related_name='events')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-date']

    def __str__(self):
        return self.title

class EventAttendee(models.Model):
    STATUS_CHOICES = (
        ('GOING', 'Going'),
        ('INTERESTED', 'Interested'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_attending')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='GOING')
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Event Attendee'
        verbose_name_plural = 'Event Attendees'
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} RSVP {self.status} for {self.event.title}"

# ---------------------------------------------------------------------
# Safety & Report Models
# ---------------------------------------------------------------------
class Report(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Review'),
        ('RESOLVED', 'Resolved'),
        ('DISMISSED', 'Dismissed'),
    )
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_submitted')
    reported_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_received')
    reported_ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reported_community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reason = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']

class SOSAlert(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='sos_alerts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sos_alerts')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'SOS Alert'
        verbose_name_plural = 'SOS Alerts'
        ordering = ['-created_at']

# ---------------------------------------------------------------------
# Rating & Review Model
# ---------------------------------------------------------------------
class Rating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    rating = models.PositiveIntegerField(help_text='Rating from 1 to 5')
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = ('reviewer', 'reviewee', 'ride')

    def __str__(self):
        return f"{self.reviewer.username} rated {self.reviewee.username} as {self.rating} stars"

# ---------------------------------------------------------------------
# System Log Models
# ---------------------------------------------------------------------
class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    email_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'

class AILog(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    log_type = models.CharField(max_length=50) # TRAVEL_ASSISTANT, MAIL_RESPONDER, CHATBOT, TOXICITY
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'AI Log'
        verbose_name_plural = 'AI Logs'

# ---------------------------------------------------------------------
# Email Verification Token (DB-persisted, not session-based)
# ---------------------------------------------------------------------
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Email Verification Token'
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"VerifyToken for {self.user.username} (used={self.is_used})"

# ---------------------------------------------------------------------
# Password Reset Token (DB-persisted with 1-hour expiry)
# ---------------------------------------------------------------------
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Password Reset Token'
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"ResetToken for {self.user.username} (used={self.is_used})"

# ---------------------------------------------------------------------
# Community Post (for announcements / feed posts)
# ---------------------------------------------------------------------
class CommunityPost(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='community_posts/', blank=True, null=True)
    is_announcement = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Community Post'
        verbose_name_plural = 'Community Posts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.username} in {self.community.name}"

# ---------------------------------------------------------------------
# Contact/Support Ticket
# ---------------------------------------------------------------------
class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    ticket_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    ai_suggested_reply = models.TextField(blank=True, default='')
    admin_reply = models.TextField(blank=True, default='')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket {self.ticket_number}: {self.subject}"

