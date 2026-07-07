from django import forms
from django.contrib.auth import get_user_model
from .models import Vehicle, Ride, Booking, RouteWaypoint, Community, Event

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'profile_picture', 'cover_image', 'bio', 
            'skills', 'interests', 'languages', 'travel_preferences'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Navigation, Safe Driving (comma-separated)'}),
            'interests': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Road trips, Music (comma-separated)'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. English, Spanish (comma-separated)'}),
            'travel_preferences': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. No smoking, Pet friendly (comma-separated)'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'license_plate', 'capacity', 'color']
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Corolla'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DL-3C-AB-1234'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available Passenger Seats'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Silver'}),
        }

class RidePublishForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            'vehicle', 'start_location', 'end_location', 'departure_time', 
            'price_per_seat', 'available_seats', 'cost_sharing', 
            'luggage_details', 'emergency_contact'
        ]
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'start_location': forms.TextInput(attrs={'class': 'form-control', 'id': 'start_location', 'placeholder': 'Enter pickup start point'}),
            'end_location': forms.TextInput(attrs={'class': 'form-control', 'id': 'end_location', 'placeholder': 'Enter final destination'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'price_per_seat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Fare in INR'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seats'}),
            'cost_sharing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Equal Split, Fuel split'}),
            'luggage_details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Max 1 bag per passenger'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency phone number'}),
        }

    def __init__(self, *args, **kwargs):
        driver = kwargs.pop('driver', None)
        super().__init__(*args, **kwargs)
        if driver:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(driver=driver)

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'rules', 'community_type', 'category', 'avatar', 'banner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DTU Alumni'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'What is this community for?'}),
            'rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter community rules...'}),
            'community_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'event_type', 'community']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weekend Trek'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the event details...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meetup Location'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'community': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only allow selecting communities the user is verified to publish in
            from .models import CommunityMember
            user_communities = CommunityMember.objects.filter(user=user, status='APPROVED').values_list('community_id', flat=True)
            self.fields['community'].queryset = Community.objects.filter(id__in=user_communities)
            self.fields['community'].required = False

