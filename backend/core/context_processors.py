"""
Global template context processors for Ride-Share platform.
Injects notification counts and user data into every template.
"""
from .models import Notification


def notification_context(request):
    """
    Inject unread notification count into every page template.
    Used by the navbar bell badge and toast system.
    """
    unread_count = 0
    recent_notifications = []

    if request.user.is_authenticated:
        try:
            unread_count = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()

            recent_notifications = list(
                Notification.objects.filter(
                    recipient=request.user
                ).order_by('-created_at')[:5].values(
                    'id', 'notification_type', 'content', 'link',
                    'is_read', 'created_at'
                )
            )
        except Exception:
            pass

    return {
        'unread_notification_count': unread_count,
        'recent_notifications': recent_notifications,
    }
