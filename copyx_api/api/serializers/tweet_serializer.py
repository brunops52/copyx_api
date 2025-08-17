from rest_framework import serializers

from .user_serializer import UserProfileSerializer
from .hashtag_serializer import HashtagSerializer
from ..models import Tweet
from ..models import Bookmark
from ..models import User

class TweetSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    like_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    mentioned_users = serializers.SerializerMethodField()
    hahstags = HashtagSerializer(many=True, read_only=True)

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
            return Bookmark.objects.filter(
                user=request.user, 
                tweet=obj
            ).exists()
        return False

    def get_mentioned_users(self, obj):
        return UserProfileSerializer(obj.mentions.all(), many=True).data
    
class UserProfileDetailSerializer(serializers.ModelSerializer):
    tweets = serializers.SerializerMethodField()
    liked_tweets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture', 'cover_photo',
            'followers_count', 'following_count',
            'tweets', 'liked_tweets'
        ]
    
    def get_tweets(self, obj):
        tweets = Tweet.objects.filter(user=obj).order_by('-created_at')
        return TweetSerializer(tweets, many=True, context=self.context).data
    
    def get_liked_tweets(self, obj):
        liked_tweets = Tweet.objects.filter(likes=obj).order_by('-created_at')
        return TweetSerializer(liked_tweets, many=True, context=self.context).data