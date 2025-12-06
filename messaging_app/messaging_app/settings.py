"""Django settings for the messaging_app project with Docker-friendly defaults."""

import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from rest_framework.pagination import PageNumberPagination


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "replace-me-with-secure-key")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"

_raw_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = [host.strip() for host in _raw_hosts.split(",") if host.strip()] or ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "messaging_app.chats",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "messaging_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "messaging_app.wsgi.application"


def _build_database_settings():
    """Return database settings reading from environment variables."""

    engine = os.getenv("DB_ENGINE") or os.getenv("DJANGO_DB_ENGINE")
    # Prefer MySQL when env vars are passed, otherwise fall back to SQLite for tests.
    if engine and engine != "django.db.backends.sqlite3":
        return {
            "ENGINE": engine,
            "NAME": os.getenv("MYSQL_DB") or os.getenv("MYSQL_DATABASE", "messaging_app"),
            "USER": os.getenv("MYSQL_USER", "messaging"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "messaging"),
            "HOST": os.getenv("MYSQL_HOST", "db"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {
                "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),
            },
        }

    if os.getenv("MYSQL_HOST"):
        return {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DB") or os.getenv("MYSQL_DATABASE", "messaging_app"),
            "USER": os.getenv("MYSQL_USER", "messaging"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "messaging"),
            "HOST": os.getenv("MYSQL_HOST", "db"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {
                "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),
            },
        }

    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }


DATABASES = {
    "default": _build_database_settings(),
}

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "messaging_app.chats.pagination.MessagePagination",
    "PAGE_SIZE": 20,
}

from rest_framework.settings import api_settings  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

# Use the custom user model defined in chats
AUTH_USER_MODEL = "messaging_app.chats.User"
