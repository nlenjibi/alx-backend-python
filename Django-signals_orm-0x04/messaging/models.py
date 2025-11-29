from django.conf import settings
from django.db import models
from django.utils import timezone


class UnreadMessagesQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(receiver=user, read=False)


class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)

    def for_user(self, user):
        return self.get_queryset().filter(receiver=user)


class MessageQuerySet(models.QuerySet):
    def with_participants(self):
        return self.select_related("sender", "receiver")

    def with_thread(self):
        # Prefetch immediate replies and their participants
        return self.prefetch_related("replies", "replies__sender", "replies__receiver")


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False, db_index=True)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    objects = MessageQuerySet.as_manager()
    unread = UnreadMessagesManager()

    class Meta:
        indexes = [
            models.Index(fields=["receiver", "read", "timestamp"]),
            models.Index(fields=["sender", "timestamp"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

    def all_replies(self):
        """Return all descendant replies using simple recursion in Python.
        For performance, call on a queryset with prefetch_related('replies').
        """
        result = []
        for child in getattr(self, "replies").all():
            result.append(child)
            result.extend(child.all_replies())
        return result


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notif for {self.user} about msg {self.message_id if hasattr(self.message, 'id') else self.message.pk}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-edited_at"]

    def __str__(self):
        return f"History of message {self.message_id if hasattr(self.message, 'id') else self.message.pk} at {self.edited_at}"
