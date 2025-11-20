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
