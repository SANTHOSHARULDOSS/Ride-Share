from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_type>\w+)/(?P<room_id>[a-zA-Z0-9_-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'^ws/tracking/(?P<ride_id>\d+)/$', consumers.TripTrackingConsumer.as_asgi()),
]
