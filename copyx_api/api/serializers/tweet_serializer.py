from rest_framework import serializers

from .user_serializer import UserProfileSerializer
from ..models import Tweet
from ..models import Bookmark

class TweetSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    like_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    mentioned_users = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'likes')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, tweet=obj).exists()
        return False

    def get_mentioned_users(self, obj):
        return UserProfileSerializer(obj.mentions.all(), many=True).data