from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    TweetListCreateView,
    TweetDetailView,
    LikeTweetView,
    )

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('tweets/', TweetListCreateView.as_view(), name='tweet-list'),
    path('tweets/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweets/<int:pk>like/', LikeTweetView.as_view(), name='tweet-like'),
]
