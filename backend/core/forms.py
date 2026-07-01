from django import forms
from django.contrib.auth import get_user_model
from .models import Vehicle, Ride, Booking, RouteWaypoint

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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
        fields = ['vehicle', 'start_location', 'end_location', 'departure_time', 'price_per_seat', 'available_seats']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'start_location': forms.TextInput(attrs={'class': 'form-control', 'id': 'start_location', 'placeholder': 'Enter pickup start point'}),
            'end_location': forms.TextInput(attrs={'class': 'form-control', 'id': 'end_location', 'placeholder': 'Enter final destination'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'price_per_seat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Fare in INR'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seats'}),
        }

    def __init__(self, *args, **kwargs):
        driver = kwargs.pop('driver', None)
        super().__init__(*args, **kwargs)
        if driver:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(driver=driver)
