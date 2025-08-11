from django.db import models

from ..models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='tweets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}...'

    @property
    def like_count(self):
        return self.lijes.count()
    
    
    