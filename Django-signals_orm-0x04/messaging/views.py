from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.contrib.auth import logout, get_user_model
from django.db.models import Q

from .models import Message


@login_required
@require_POST
def delete_user(request):
    """Allow an authenticated user to delete their own account.

    Returns a JSON payload indicating success. The related data
    (messages, notifications, histories) are cleaned by signals or
    FK cascade as configured in the app.
    """
    user = request.user
    user_id = user.id
    # End the session first, then delete the account
    logout(request)
    user.delete()
    return JsonResponse({"status": "deleted", "user_id": user_id})


@login_required
@cache_page(60)
def conversation_messages(request, user_id: int):
    """List messages in a conversation with a specific user.

    Optimized using select_related for FK joins and prefetch_related
    for reverse relations (replies).
    """
    User = get_user_model()
    other = User.objects.filter(pk=user_id).first()
    if other is None:
        return JsonResponse({"error": "User not found"}, status=404)

    qs = (
        Message.objects.filter(
            Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user)
        )
        .select_related("sender", "receiver")
        .prefetch_related("replies", "replies__sender", "replies__receiver")
    )

    data = [
        {
            "id": m.id,
            "sender": m.sender_id,
            "receiver": m.receiver_id,
            "content": m.content,
            "timestamp": getattr(m, "timestamp", None).isoformat() if getattr(m, "timestamp", None) else None,
        }
        for m in qs
    ]
    return JsonResponse({"messages": data})


@login_required
@cache_page(60)
def message_thread(request, message_id: int):
    """Return a threaded representation of a message and all its replies.

    Uses select_related for participants and prefetch_related for nested replies,
    then builds a nested structure via recursion.
    """
    root = (
        Message.objects.filter(pk=message_id)
        .select_related("sender", "receiver")
        .prefetch_related("replies", "replies__sender", "replies__receiver", "replies__replies")
        .first()
    )
    if root is None:
        return JsonResponse({"error": "Message not found"}, status=404)

    def serialize(node: Message):
        return {
            "id": node.id,
            "sender": node.sender_id,
            "receiver": node.receiver_id,
            "content": node.content,
            "timestamp": getattr(node, "timestamp", None).isoformat() if getattr(node, "timestamp", None) else None,
            "replies": [serialize(child) for child in node.replies.all()],
        }

    return JsonResponse(serialize(root))


@login_required
def unread_inbox(request):
    """Return unread messages for the current user using the custom manager,
    optimized with only() and select_related().
    """
    qs = (
        Message.unread.unread_for_user(request.user)
        .only("id", "sender_id", "receiver_id", "content", "timestamp")
        .select_related("sender", "receiver")
    )
    data = [
        {
            "id": m.id,
            "sender": m.sender_id,
            "receiver": m.receiver_id,
            "content": m.content,
            "timestamp": getattr(m, "timestamp", None).isoformat() if getattr(m, "timestamp", None) else None,
        }
        for m in qs
    ]
    return JsonResponse({"unread": data})
