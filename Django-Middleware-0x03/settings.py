"""Minimal settings for Django-Middleware-0x03 demo project."""

SECRET_KEY = "replace-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "messaging_app.chats",
]

MIDDLEWARE = [
    "Django-Middleware-0x03.chats.middleware.RequestLoggingMiddleware",
    "Django-Middleware-0x03.chats.middleware.RestrictAccessByTimeMiddleware",
    "Django-Middleware-0x03.chats.middleware.OffensiveLanguageMiddleware",
    "Django-Middleware-0x03.chats.middleware.RolepermissionMiddleware",
]

ROOT_URLCONF = ""
