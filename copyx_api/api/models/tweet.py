from django.db import models

from ..models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='tweets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    mentions = models.ManyToManyField(User, related_name='mentioned_in_tweets', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}...'

    @property
    def like_count(self):
        return self.lijes.count()
    
    
    def extract_mentions(self):
        import re
        usernames = re.findall(r'@(\w+)', self.content)
        return User.objects.filter(username__in=usernames)
    
    def extract_hashtags(self):
        import re
        hashtags = re.findall(r'#(\w+)', self.content.lower())
        return list(set(hashtags))