import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, User, Community, Ride, Notification

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_type = self.scope['url_route']['kwargs']['room_type']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        
        # Resolve distinct room name
        if self.room_type == 'direct':
            # Create a unique sorted channel identifier for direct messaging
            ids = sorted([str(self.user.id), str(self.room_id)])
            self.room_group_name = f"chat_direct_{ids[0]}_{ids[1]}"
        elif self.room_type == 'community':
            self.room_group_name = f"chat_community_{self.room_id}"
        elif self.room_type == 'ride':
            self.room_group_name = f"chat_ride_{self.room_id}"
        else:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type", "message")

        if event_type == "typing":
            # Broadcast typing indicator to others in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_typing",
                    "sender_id": str(self.user.id),
                    "username": self.user.username,
                    "is_typing": data.get("is_typing", False)
                }
            )
        elif event_type == "message":
            content = data.get("content", "")
            file_name = data.get("file_name", "")
            file_type = data.get("file_type", "")
            # file_data can be a base64 encoded data url, or URL string
            file_url = data.get("file_url", "")

            # Save message to DB
            msg = await self.save_message(content, file_url, file_name, file_type)
            
            # Send message data to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "id": msg.id,
                    "sender_id": str(self.user.id),
                    "username": self.user.username,
                    "profile_picture": self.user.profile_picture.url if self.user.profile_picture else "/static/images/icons/default-avatar.png",
                    "content": content,
                    "file_url": file_url,
                    "file_name": file_name,
                    "file_type": file_type,
                    "created_at": msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

            # Trigger real-time notifications for offline or inactive recipients
            if self.room_type == 'direct':
                recipient_id = self.room_id
                await self.send_in_app_notification(recipient_id, f"New message from {self.user.username}: {content[:50]}...")

    @database_sync_to_async
    def save_message(self, content, file_url, file_name, file_type):
        recipient = None
        community = None
        ride = None

        if self.room_type == 'direct':
            recipient = User.objects.get(id=self.room_id)
        elif self.room_type == 'community':
            community = Community.objects.get(id=self.room_id)
        elif self.room_type == 'ride':
            ride = Ride.objects.get(id=self.room_id)

        msg = Message.objects.create(
            sender=self.user,
            recipient=recipient,
            community=community,
            ride=ride,
            content=content,
            file_name=file_name,
            file_type=file_type
        )
        if file_url:
            # Storing URL in database (for simplicity, we can store it directly in Content or field)
            # If the client uploaded a file, we save the url references
            msg.file_name = file_name
            msg.file_type = file_type
            # We can save path relative or keep string
        msg.save()
        return msg

    async def send_in_app_notification(self, recipient_id, content):
        # Notify recipient via Notification Consumer channel group
        recipient_group = f"user_notifications_{recipient_id}"
        
        # Save notification to DB
        notif = await self.create_db_notification(recipient_id, content)

        await self.channel_layer.group_send(
            recipient_group,
            {
                "type": "new_notification",
                "id": notif.id,
                "notification_type": "MESSAGE",
                "sender_id": str(self.user.id),
                "sender_username": self.user.username,
                "content": content,
                "created_at": notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    @database_sync_to_async
    def create_db_notification(self, recipient_id, content):
        recipient = User.objects.get(id=recipient_id)
        return Notification.objects.create(
            recipient=recipient,
            sender=self.user,
            notification_type="MESSAGE",
            content=content
        )

    # Handlers for events sent from channel layer
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "id": event["id"],
            "sender_id": event["sender_id"],
            "username": event["username"],
            "profile_picture": event["profile_picture"],
            "content": event["content"],
            "file_url": event.get("file_url"),
            "file_name": event.get("file_name"),
            "file_type": event.get("file_type"),
            "created_at": event["created_at"],
        }))

    async def chat_typing(self, event):
        if event["sender_id"] != str(self.user.id):
            await self.send(text_data=json.dumps({
                "type": "typing",
                "sender_id": event["sender_id"],
                "username": event["username"],
                "is_typing": event["is_typing"]
            }))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_group_name = f"user_notifications_{self.user.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send initial unread count on connect
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': unread_count
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        if action == "mark_as_read":
            notif_id = data.get("notification_id")
            await self.mark_read(notif_id)
        elif action == "mark_all_read":
            await self.mark_all_read()
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({'type': 'unread_count', 'count': unread_count}))

    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(recipient=self.user, is_read=False).count()

    @database_sync_to_async
    def mark_read(self, notif_id):
        try:
            notif = Notification.objects.get(id=notif_id, recipient=self.user)
            notif.is_read = True
            notif.save()
        except Notification.DoesNotExist:
            pass

    @database_sync_to_async
    def mark_all_read(self):
        Notification.objects.filter(recipient=self.user, is_read=False).update(is_read=True)

    async def new_notification(self, event):
        """Push a new notification to this user's browser."""
        notif_type = event.get('notification_type', 'INFO')
        # Map notification type to toast style
        toast_map = {
            'FRIEND_REQUEST': 'info',
            'TRIP_REQUEST': 'info',
            'TRIP_ACCEPTED': 'success',
            'MESSAGE': 'info',
            'COMMUNITY_INVITE': 'info',
            'ADMIN_ANNOUNCEMENT': 'warning',
        }
        await self.send(text_data=json.dumps({
            "type": "notification",
            "id": event.get("id"),
            "notification_type": notif_type,
            "title": event.get("title", "RideShare"),
            "message": event.get("content", ""),
            "toast_type": toast_map.get(notif_type, 'info'),
            "sender_id": event.get("sender_id"),
            "sender_username": event.get("sender_username"),
            "content": event.get("content", ""),
            "created_at": event.get("created_at", ""),
        }))




class TripTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f"trip_tracking_{self.ride_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Driver broadcasts coordinates: {"latitude": 12.34, "longitude": 56.78, "driver_name": "John"}
        data = json.loads(text_data)
        lat = data.get("latitude")
        lng = data.get("longitude")
        driver_name = data.get("driver_name", "Driver")
        sos_triggered = data.get("sos", False)

        # Broadcast telemetry to passengers
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "trip_telemetry",
                "latitude": lat,
                "longitude": lng,
                "driver_name": driver_name,
                "sos": sos_triggered
            }
        )

    async def trip_telemetry(self, event):
        await self.send(text_data=json.dumps({
            "type": "telemetry",
            "latitude": event["latitude"],
            "longitude": event["longitude"],
            "driver_name": event["driver_name"],
            "sos": event["sos"]
        }))
