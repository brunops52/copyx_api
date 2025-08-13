from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    bio = models.TextField(max_length=160, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def follow(self, user_to_follow):
        if self != user_to_follow:
            self.following.add(user_to_follow)
            return True
        return False
    
    def unfollow(self, user_to_unfollow):
        self.following.remove(user_to_unfollow)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()
    