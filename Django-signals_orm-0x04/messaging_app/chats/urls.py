from django.urls import path
from .views import conversation_view

app_name = "chats"

urlpatterns = [
    path("conversation/<int:user_id>/", conversation_view, name="conversation"),
]