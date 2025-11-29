from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model

from messaging.models import Message


@cache_page(60)
def conversation_view(request, user_id: int):
    # Show messages between request.user and target user
    User = get_user_model()
    other = User.objects.filter(pk=user_id).first()
    if not request.user.is_authenticated or other is None:
        return JsonResponse({"error": "Unauthorized or user not found"}, status=401)

    # Messages where participants are the pair; eager-load participants and replies
    qs = Message.objects.with_participants().filter(
        sender_id__in=[request.user.id, other.id], receiver_id__in=[request.user.id, other.id]
    ).with_thread()

    data = [
        {
            "id": m.id,
            "sender": m.sender_id,
            "receiver": m.receiver_id,
            "content": m.content,
            "timestamp": m.timestamp.isoformat(),
            "replies": [
                {
                    "id": r.id,
                    "sender": r.sender_id,
                    "receiver": r.receiver_id,
                    "content": r.content,
                    "timestamp": r.timestamp.isoformat(),
                }
                for r in m.replies.all()
            ],
        }
        for m in qs
    ]
    return JsonResponse({"messages": data})