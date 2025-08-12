from rest_framework import serializers

from .user_serializer import UserProfileSerializer
from ..models.notification import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserProfileSerializer(read_only=True)
    message = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'notification_type', 'tweet', 'created_at', 'message']
        read_only_fields = fields
        