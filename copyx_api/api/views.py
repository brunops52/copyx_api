from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,
    UserProfileSerializer,
    TweetSerializer,
    CommentSerializer,
    BookmarkSerializer,
    NotificationSerializer,
    FollowSerializer
)
from .models import User, Tweet, Comment, Bookmark, Notification

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TweetListCreateView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TweetDetailView(generics.RetrieveDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Você não tem permissão para esta ação.")
        instance.delete()

class LikeTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
            action = 'unliked'
        else:
            tweet.likes.add(request.user)
            action = 'liked'
        return Response({'status': f'Tweet {action}.'})
    
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_pk = self.kwargs['tweet_pk']
        return Comment.objects.filter(tweet__pk=tweet_pk)
    
    def perform_create(self, serializer):
        tweet = get_object_or_404(Tweet, pk=self.kwargs['tweet_pk'])
        serializer.save(user=self.request.user, tweet=tweet)

class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Você não tem permissão para esta ação.")
        instance.delete()

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'], tweet__pk=self.kwargs['tweet_pk'])
        return comment      
    
class BookmarkListView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)
    
class BookmarkToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            bookmark.delete()
            action = 'removed'
        else:
            action = 'added'

        return Response({'status': f'Bookmark {action}.'})
    
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, pk=pk)
        
        if request.user == user_to_follow:
            return Response(
                {'error': 'Você não pode seguir a si mesmo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.is_following(user_to_follow):
            request.user.unfollow(user_to_follow)
            action = 'unfollowed'
        else:
            request.user.follow(user_to_follow)
            action = 'followed'

        return Response({
            'status': f"Successfully {action} {user_to_follow.username}.",
            'is_following': request.user.is_following(user_to_follow),
            'followers_count': user_to_follow.followers_count,
            'following_count': request.user.following_count
        })
    
class userRelationsView(APIView):
    serializer_class = FollowSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user



