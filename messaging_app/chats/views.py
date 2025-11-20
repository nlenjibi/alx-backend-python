from django.apps import apps
from rest_framework import viewsets, serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .auth import JWTOrSessionAuthentication
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


Message = apps.get_model("messaging_app.chats", "Message")
Conversation = apps.get_model("messaging_app.chats", "Conversation")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for messages with pagination, filtering and participant permission."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTOrSessionAuthentication]
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["-timestamp"]
    search_fields = ["content"]


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations. Only participants can access."""

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTOrSessionAuthentication]
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["-updated", "-created"]
    search_fields = ["title"]

    filterset_class = MessageFilter
    ordering_fields = ["timestamp"]
    search_fields = ["content"]


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations. Only participants can access."""

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTOrSessionAuthentication]
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
*** End Patch