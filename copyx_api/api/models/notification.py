from django.db import models

from .user import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Novo seguidor'),
        ('like', 'Curtiu seu tweet'),
        ('comment', 'Comentou no seu tweet'),
        ('mention', 'Mencionou você'),
    )

    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='acted_notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    tweet = models.ForeignKey('Tweet', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} {self.get_notification_type_display()}"
    
    @property
    def message(self):
        verb = dict(self.NOTIFICATION_TYPES)[self.notification_type]
        return f"{self.actor.username} {verb}"