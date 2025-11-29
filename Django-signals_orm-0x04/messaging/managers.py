from django.db import models


class UnreadMessagesQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(receiver=user, read=False)


class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)

    def for_user(self, user):
        return self.get_queryset().filter(receiver=user)

    def unread_for_user(self, user):
        return self.for_user(user)


class MessageQuerySet(models.QuerySet):
    def with_participants(self):
        return self.select_related("sender", "receiver")

    def with_thread(self):
        return self.prefetch_related("replies", "replies__sender", "replies__receiver")
