from django.apps import apps
from rest_framework import viewsets, serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ["-timestamp"]
    search_fields = ["content"]

    def get_queryset(self):
        """Optionally filter messages by `conversation_id` query parameter."""
        qs = Message.objects.all()
        conv_id = self.request.query_params.get("conversation_id") or self.request.query_params.get("conversation")
        if conv_id:
            # use Message.objects.filter to select messages for the conversation
            try:
                return Message.objects.filter(conversation__id=conv_id)
            except Exception:
                return qs
        return qs

    def create(self, request, *args, **kwargs):
        # Ensure the requesting user is a participant of the conversation
        conv_id = request.data.get("conversation") or request.data.get("conversation_id") or request.data.get("conversationId")
        if not conv_id:
            return Response({"detail": "conversation_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Conversation = apps.get_model("messaging_app.chats", "Conversation")
            conv = Conversation.objects.get(pk=conv_id)
        except Exception:
            return Response({"detail": "conversation not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            is_participant = request.user in conv.participants.all()
        except Exception:
            is_participant = request.user in conv.participants

        if not is_participant:
            # Explicitly return HTTP 403 when user is not a participant
            return Response({"detail": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations. Only participants can access."""

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTOrSessionAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["-updated", "-created"]
    search_fields = ["title"]
    filterset_class = MessageFilter
