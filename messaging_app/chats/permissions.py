from rest_framework import permissions


class IsOwnerOrParticipant(permissions.BasePermission):
    """Allow access only to owners or participants of a conversation/message.

    Intended to be used with `permission_classes` on viewsets or views handling
    conversation and message objects. The permission checks common attribute
    names such as `user`, `owner`, or `participants`.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Message-like objects with a `user` or `sender` attribute
        if hasattr(obj, "user"):
            return obj.user == user
        if hasattr(obj, "sender"):
            return obj.sender == user

        # Conversation-like objects with `owner` or `participants`
        if hasattr(obj, "owner"):
            return obj.owner == user

        if hasattr(obj, "participants"):
            participants = obj.participants
            # If it's a manager (ManyToMany), call `.all()`
            try:
                return user in participants.all()
            except Exception:
                return user in participants

        # Fallback deny
        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """Allow access only to authenticated users who are participants of a conversation.

    This permission should be applied to message and conversation viewsets so that
    only participants can view, create, update or delete messages in a conversation.
    """

    def has_permission(self, request, view):
        # Require authentication for all actions
        user = request.user
        if not (user and user.is_authenticated):
            return False

        # When creating (sending) a message, ensure the user is a participant
        # of the conversation they're trying to send to.
        if request.method == "POST":
            conv_id = None
            # common keys for conversation reference in payload
            for key in ("conversation", "conversation_id", "conversationId"):
                if key in request.data:
                    conv_id = request.data.get(key)
                    break

            if not conv_id:
                # No conversation specified — deny creation to be safe
                return False

            try:
                Conversation = apps.get_model("messaging_app.chats", "Conversation")
            except Exception:
                return False

            try:
                conv = Conversation.objects.get(pk=conv_id)
            except Exception:
                return False

            try:
                return user in conv.participants.all()
            except Exception:
                return user in conv.participants

        # For other methods, defer to object-level permission checks where needed
        return True

    def has_object_permission(self, request, view, obj):
        # Ensure user is participant of the conversation or owner
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Only participants/owners may perform write or read operations.
        # Explicitly check HTTP methods including PUT, PATCH, DELETE.
        if request.method in ("PUT", "PATCH", "DELETE", "GET", "POST"):
            # If object is a Message-like instance
            if hasattr(obj, "conversation"):
                conv = obj.conversation
                # Conversation has participants or owner
                if hasattr(conv, "participants"):
                    try:
                        return user in conv.participants.all()
                    except Exception:
                        return user in conv.participants
                if hasattr(conv, "owner"):
                    return conv.owner == user

            # If object is a Conversation-like instance
            if hasattr(obj, "participants"):
                participants = obj.participants
                try:
                    return user in participants.all()
                except Exception:
                    return user in participants

            if hasattr(obj, "owner"):
                return obj.owner == user

            # If Message has 'sender' or 'user' attribute
            if hasattr(obj, "sender"):
                return obj.sender == user
            if hasattr(obj, "user"):
                return obj.user == user

            # Fallback deny
            return False

        # For any other HTTP methods, deny by default
        return False
