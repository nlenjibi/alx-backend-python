from django.contrib import admin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "created_at")
    search_fields = ("username", "email")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "conversation", "sent_at")
    search_fields = ("message_body",)
