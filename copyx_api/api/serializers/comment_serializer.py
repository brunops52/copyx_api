from rest_framework import serializers

from .user_serializer import UserProfileSerializer
from ..models import Comment



class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'tweet', 'created_at')
        