# Minimal settings to demonstrate caching config for the exercise
SECRET_KEY = "dummy"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

MIDDLEWARE = []

ROOT_URLCONF = "messaging_app.urls"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
