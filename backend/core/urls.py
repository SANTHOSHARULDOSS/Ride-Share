from django.urls import path
from . import views

urlpatterns = [
    # General & Auth
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/passenger/', views.dashboard_passenger, name='dashboard_passenger'),
    path('dashboard/driver/', views.dashboard_driver, name='dashboard_driver'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    
    # Profile & Vehicle Settings
    path('profile/', views.profile_view, name='profile'),
    
    # Ride Operations
    path('ride/search/', views.ride_search_view, name='ride_search'),
    path('ride/publish/', views.ride_publish_view, name='ride_publish'),
    path('ride/<int:pk>/', views.ride_details_view, name='ride_details'),
    path('ride/<int:pk>/status/', views.ride_status_update_view, name='ride_status_update'),
    
    # Booking Operations
    path('booking/create/<int:ride_id>/', views.booking_create_view, name='booking_create'),
    path('booking/<int:booking_id>/action/', views.booking_action_view, name='booking_action'),
    
    # Checkout Payment Gateway Mock Screen
    path('payment/<int:booking_id>/', views.payment_simulate_view, name='payment_simulate'),
    
    # Admin resets
    path('admin/reset/', views.admin_reset_view, name='admin_reset'),
    
    # Offline Support
    path('offline/', views.offline_view, name='offline'),
    
    # Project Report Presentation
    path('report/', views.project_report_view, name='project_report'),
]
