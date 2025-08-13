from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tweets = models.ManyToManyField('Tweet', related_name='hashtag')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name