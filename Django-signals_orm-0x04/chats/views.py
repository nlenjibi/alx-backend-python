from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page


# Example cached view for listing messages in a conversation
@require_GET
@cache_page(60)
def messages_list(request):
    # In a real app, query DB for conversation messages here
    payload = {
        "status": "ok",
        "cached": True,
        "message": "This list is cached for 60 seconds.",
    }
    return JsonResponse(payload)
