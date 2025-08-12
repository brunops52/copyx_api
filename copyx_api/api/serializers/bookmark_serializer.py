from rest_framework import serializers

from .tweet_serializer import TweetSerializer
from ..models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = '__all__'
        read_only_fields = ('user', 'created_at')