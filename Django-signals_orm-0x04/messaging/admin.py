from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "short_content", "timestamp", "edited", "read", "parent_message")
    list_filter = ("edited", "read", "timestamp")
    search_fields = ("content", "sender__username", "receiver__username")
    autocomplete_fields = ("sender", "receiver", "parent_message")

    def short_content(self, obj):
        return (obj.content or "")[:40]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    autocomplete_fields = ("user", "message")


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "edited_at", "snippet")
    search_fields = ("old_content",)
    autocomplete_fields = ("message",)

    def snippet(self, obj):
        return (obj.old_content or "")[:40]
