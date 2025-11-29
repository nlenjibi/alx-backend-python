from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Message, Notification, MessageHistory


class MessagingSignalsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.sender = User.objects.create_user(username="alice", password="x")
        self.receiver = User.objects.create_user(username="bob", password="x")

    def test_notification_created_on_new_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="hi", timestamp=timezone.now())
        self.assertTrue(Notification.objects.filter(user=self.receiver, message=msg).exists())

    def test_history_created_on_edit(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="first", timestamp=timezone.now())
        msg.content = "second"
        msg.save()
        self.assertTrue(msg.edited)
        self.assertEqual(msg.history.count(), 1)

    def test_unread_manager_for_user(self):
        Message.objects.create(sender=self.sender, receiver=self.receiver, content="one")
        Message.objects.create(sender=self.sender, receiver=self.receiver, content="two", read=True)
        self.assertEqual(Message.unread.for_user(self.receiver).count(), 1)
