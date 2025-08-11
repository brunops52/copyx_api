from django.db import models


from ..models import User
from .tweet import Tweet

class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')