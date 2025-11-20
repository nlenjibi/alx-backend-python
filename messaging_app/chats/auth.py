from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTOrSessionAuthentication(BaseAuthentication):
    """Try JWT authentication first, fall back to session authentication.

    This authentication class can be referenced in Django settings or view `authentication_classes`.
    """

    def authenticate(self, request):
        # Try JWT first
        jwt_auth = JWTAuthentication().authenticate(request)
        if jwt_auth is not None:
            return jwt_auth

        # Fall back to session auth
        return SessionAuthentication().authenticate(request)
