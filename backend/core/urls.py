from django.urls import path
from . import views, auth_views, views_extended

urlpatterns = [
    # General & Base Pages
    path('', views.landing_view, name='landing'),
    path('offline/', views.offline_view, name='offline'),
    path('contact/', views_extended.contact_view, name='contact'),

    # Authentication & Session Lifecycle
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path('verify-email/', auth_views.verify_email_page, name='verify_email_page'),
    path('verify-email/resend/', auth_views.resend_verification_view, name='resend_verification'),
    path('forgot-password/', auth_views.forgot_password_view, name='forgot_password'),
    path('reset-password/', auth_views.reset_password_view, name='reset_password'),
    path('change-password/', auth_views.change_password_view, name='change_password'),
    path('google-login/', auth_views.google_login_view, name='google_login'),
    path('sessions/', auth_views.sessions_view, name='sessions'),
    path('sessions/<int:session_id>/terminate/', auth_views.terminate_session_view, name='terminate_session'),

    # AJAX Helpers
    path('api/check-username/', auth_views.check_username_view, name='check_username'),

    # Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/passenger/', views.dashboard_passenger, name='dashboard_passenger'),
    path('dashboard/driver/', views.dashboard_driver, name='dashboard_driver'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('api/admin/stats/', views.admin_stats_api, name='admin_stats_api'),

    # Profile & Vehicle Settings
    path('profile/', views.profile_view, name='profile'),

    # Ride Operations
    path('ride/search/', views.ride_search_view, name='ride_search'),
    path('ride/publish/', views.ride_publish_view, name='ride_publish'),
    path('ride/<int:pk>/', views.ride_details_view, name='ride_details'),
    path('ride/<int:pk>/status/', views.ride_status_update_view, name='ride_status_update'),
    path('ride/<int:ride_id>/rate/', views_extended.rate_trip_view, name='rate_trip'),

    # Booking Operations
    path('booking/create/<int:ride_id>/', views.booking_create_view, name='booking_create'),
    path('booking/<int:booking_id>/action/', views.booking_action_view, name='booking_action'),
    path('payment/<int:booking_id>/', views.payment_simulate_view, name='payment_simulate'),

    # Community System
    path('communities/', views_extended.community_list_view, name='community_list'),
    path('communities/create/', views_extended.community_create_view, name='community_create'),
    path('communities/<str:comm_id>/', views_extended.community_detail_view, name='community_detail'),
    path('communities/<str:comm_id>/join/', views_extended.community_join_view, name='community_join'),
    path('communities/<str:comm_id>/leave/', views_extended.community_leave_view, name='community_leave'),
    path('communities/<str:comm_id>/approve/<str:user_id>/', views_extended.community_approve_member_view, name='community_approve_member'),
    path('communities/<str:comm_id>/post/', views_extended.community_post_view, name='community_post'),
    path('communities/<str:comm_id>/post/<int:post_id>/like/', views_extended.community_post_like_view, name='community_post_like'),

    # Friend System
    path('friends/', views_extended.friends_list_view, name='friends'),
    path('friends/request/<str:user_id>/', views_extended.friend_request_view, name='friend_request'),
    path('friends/accept/<int:friendship_id>/', views_extended.friend_accept_view, name='friend_accept'),
    path('friends/reject/<int:friendship_id>/', views_extended.friend_reject_view, name='friend_reject'),
    path('friends/remove/<str:user_id>/', views_extended.friend_remove_view, name='friend_remove'),

    # Event Planner
    path('events/', views_extended.event_list_view, name='event_list'),
    path('events/create/', views_extended.event_create_view, name='event_create'),
    path('events/<str:event_id>/', views_extended.event_detail_view, name='event_detail'),
    path('events/<str:event_id>/rsvp/<str:status_choice>/', views_extended.event_rsvp_view, name='event_rsvp'),

    # Chat Operations
    path('chat/', views_extended.chat_dashboard_view, name='chat_dashboard'),
    path('chat/<str:room_type>/<str:room_id>/', views_extended.chat_room_view, name='chat_room'),
    path('chat/upload/', views_extended.chat_upload_file_view, name='chat_upload'),

    # Notifications
    path('notifications/', views_extended.notifications_view, name='notifications'),
    path('notifications/<int:notif_id>/read/', views_extended.mark_notification_read_view, name='mark_notification_read'),
    path('notifications/read-all/', views_extended.mark_all_notifications_read_view, name='mark_all_notifications_read'),

    # Safety & SOS & Reporting
    path('safety/sos/', views_extended.sos_trigger_view, name='sos_trigger'),
    path('safety/report/', views_extended.report_submit_view, name='report_submit'),

    # Reputation & ID Verification
    path('reputation/', views_extended.reputation_dashboard_view, name='reputation'),
    path('reputation/verify-id/', views_extended.verify_id_upload_view, name='verify_id'),
    path('reputation/verify-org/', views_extended.verify_org_email_view, name='verify_org'),

    # AI Helpers
    path('support/chatbot/', views_extended.ai_support_chatbot_view, name='support_chatbot'),
    path('support/trip-assistant/', views_extended.ai_trip_planner_view, name='trip_assistant'),

    # Admin Audit logs & email simulation
    path('admin/logs/', views_extended.admin_system_logs_view, name='admin_system_logs'),
    path('admin/logs/simulate-email/', views_extended.admin_email_reply_processor, name='admin_simulate_email'),
    path('admin/logs/reply/<int:ticket_id>/', views_extended.admin_reply_ticket_view, name='admin_reply_ticket'),
    path('admin/logs/status/<int:ticket_id>/', views_extended.admin_update_ticket_status_view, name='admin_update_ticket'),
    path('admin/reset/', views.admin_reset_view, name='admin_reset'),
]
