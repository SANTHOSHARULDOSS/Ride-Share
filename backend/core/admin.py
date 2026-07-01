from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Vehicle, Ride, RouteWaypoint, Booking

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Profile Info', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Profile Info', {
            'classes': ('wide',),
            'fields': ('role', 'phone_number', 'profile_picture'),
        }),
    )

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('driver', 'make', 'model', 'license_plate', 'capacity', 'color')
    search_fields = ('driver__username', 'make', 'model', 'license_plate')

class RouteWaypointInline(admin.TabularInline):
    model = RouteWaypoint
    extra = 1

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'vehicle', 'start_location', 'end_location', 'departure_time', 'price_per_seat', 'available_seats', 'status')
    list_filter = ('status', 'departure_time')
    search_fields = ('driver__username', 'start_location', 'end_location')
    inlines = [RouteWaypointInline]

@admin.register(RouteWaypoint)
class RouteWaypointAdmin(admin.ModelAdmin):
    list_display = ('ride', 'sequence_order', 'name', 'latitude', 'longitude', 'estimated_arrival')
    list_filter = ('ride',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'passenger', 'pickup_location', 'dropoff_location', 'seats_requested', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('passenger__username', 'pickup_location', 'dropoff_location')

