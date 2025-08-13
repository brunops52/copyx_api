from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    TweetListCreateView,
    TweetDetailView,
    LikeTweetView,
    CommentListCreateView,
    CommentDetailView,
    BookmarkListView,
    BookmarkToggleView,
    NotificationListView,
    FollowToggleView,
    userRelationsView
    )

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('tweets/', TweetListCreateView.as_view(), name='tweet-list'),
    path('tweets/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweets/<int:pk>/like/', LikeTweetView.as_view(), name='tweet-like'),
    path('tweets/<int:tweet_pk>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('tweets/<int:tweet_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('bookmarks/', BookmarkListView.as_view(), name='bookmark-list'),
    path('tweets/<int:pk>/bookmark/', BookmarkToggleView.as_view(), name='tweet-bookmark'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('users/<int:pk>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
    path('users/<int:pk>/relationships/', userRelationsView.as_view(), name='user-relarionships'),

]
