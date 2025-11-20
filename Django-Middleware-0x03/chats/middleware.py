import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict, deque
import time

logger = logging.getLogger(__name__)

# Simple in-memory store for rate limiting — suitable for demo/tests only
_rate_store = defaultdict(lambda: deque())


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log each incoming request to a file `requests.log` with timestamp, user and path."""

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.log_file = "requests.log"

    def __call__(self, request):
        user = getattr(request, "user", None)
        user_repr = user.username if getattr(user, "is_authenticated", False) else "Anonymous"
        entry = f"{datetime.now()} - User: {user_repr} - Path: {request.path}\n"
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception:
            logger.exception("Failed to write request log")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """Deny access to the chat outside of allowed hours (6:00 - 21:00 server time).

    If current hour is not within 6..20 inclusive, return 403 Forbidden.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # allowed hours: 6 (6:00) to 21 (21:00) exclusive upper bound
        self.start_hour = 6
        self.end_hour = 21

    def __call__(self, request):
        now = datetime.now()
        if not (self.start_hour <= now.hour < self.end_hour):
            return HttpResponseForbidden("Chat is available between 06:00 and 21:00 server time.")
        return self.get_response(request)


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """Rate limit POST requests (messages) from an IP: e.g., 5 messages per 60 seconds.

    This is a demonstration implementation using an in-memory store keyed by remote IP.
    For production use, use a shared cache (Redis) to maintain limits across processes.
    """

    def __init__(self, get_response=None, limit=5, window_seconds=60):
        super().__init__(get_response)
        self.limit = limit
        self.window_seconds = window_seconds

    def __call__(self, request):
        # Only apply to POST requests (message creation)
        if request.method == "POST":
            ip = self._get_ip(request)
            now = time.time()
            dq = _rate_store[ip]
            # pop old timestamps
            while dq and dq[0] <= now - self.window_seconds:
                dq.popleft()
            if len(dq) >= self.limit:
                return JsonResponse({"detail": "Rate limit exceeded. Try again later."}, status=429)
            dq.append(now)
        return self.get_response(request)

    def _get_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "127.0.0.1")


class RolepermissionMiddleware(MiddlewareMixin):
    """Check user role from request.user and allow only admins/moderators for certain actions.

    This middleware demonstrates blocking non-admins from sensitive endpoints (example: '/admin-chat/')
    """

    def __init__(self, get_response=None, allowed_roles=None):
        super().__init__(get_response)
        if allowed_roles is None:
            allowed_roles = ("admin", "moderator")
        self.allowed_roles = set(allowed_roles)

    def __call__(self, request):
        path = request.path
        # Example: endpoints starting with /admin-chat/ require elevated roles
        if path.startswith("/admin-chat/"):
            user = getattr(request, "user", None)
            if not (user and getattr(user, "is_authenticated", False)):
                return HttpResponseForbidden("Authentication required")
            # Expect the user to have a `role` attribute, or use staff/superuser
            role = getattr(user, "role", None)
            if role:
                if role not in self.allowed_roles:
                    return HttpResponseForbidden("Insufficient role privileges")
            else:
                # Fallback to Django staff/superuser flags
                if not (getattr(user, "is_staff", False) or getattr(user, "is_superuser", False)):
                    return HttpResponseForbidden("Insufficient privileges")
        return self.get_response(request)
