from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import logout


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
