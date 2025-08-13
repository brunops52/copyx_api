from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import Notification, Tweet, User, Comment

@receiver(m2m_changed, sender=Tweet.likes.through)
def create_like_notification(sender, instance, action, pk_set, **kwargs):
    for user_pk in pk_set:
        if action == 'post_add':
            user = User.objects.get(pk=user_pk)
            if user != instance.user:
                Notification.objects.create(
                    user=instance.user,
                    actor=user,
                    notification_type='like',
                    tweet=instance
                )

@receiver(m2m_changed, sender=User.followers.through)
def create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_pk in pk_set:
            follower = User.objects.get(pk=user_pk)
            Notification.objects.create(
                user=instance,
                actor=follower,
                notification_type='follow'
            )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.tweet.user != instance.user:
        Notification.objects.create(
            user=instance.tweet.user,
            actor=instance.user,
            notification_type='comment',
            tweet=instance.tweet
        )