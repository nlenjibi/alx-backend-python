from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import MessageViewSet, ConversationViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Nested router so messages can be accessed under conversations/{conversation_pk}/messages/
nested_router = NestedDefaultRouter(router, r"conversations", lookup="conversation")
nested_router.register(r"messages", MessageViewSet, basename="conversation-messages")

urlpatterns = [
	path("", include(router.urls)),
	path("", include(nested_router.urls)),
]
