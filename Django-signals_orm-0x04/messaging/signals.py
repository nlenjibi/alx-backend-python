from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message_create(sender, instance: Message, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance: Message, **kwargs):
    if instance.pk:
        try:
            old = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        if old.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old.content)
            instance.edited = True


User = get_user_model()


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Explicit cleanup to demonstrate signals (CASCADE could suffice)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    # Histories are removed by cascade via Message FK; nothing else required
