from django.urls import path, include

urlpatterns = [
    path("", include("messaging_app.chats.urls")),
]