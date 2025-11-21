from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .auth import JWTOrSessionAuthentication
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for messages with pagination, filtering and participant permission."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTOrSessionAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ["-sent_at"]
    search_fields = ["message_body"]

    def get_queryset(self):
        """Optionally filter messages by `conversation_id` query parameter."""
        qs = Message.objects.all()
        # support query param or nested URL lookup (conversation_pk)
        conv_id = (
            self.request.query_params.get("conversation_id")
            or self.request.query_params.get("conversation")
            or self.kwargs.get("conversation_pk")
        )
        if conv_id:
            try:
                return Message.objects.filter(conversation__conversation_id=conv_id)
            except Exception:
                return qs
        return qs

    def create(self, request, *args, **kwargs):
        # Ensure the requesting user is a participant of the conversation
        conv_id = (
            request.data.get("conversation")
            or request.data.get("conversation_id")
            or request.data.get("conversationId")
            or self.kwargs.get("conversation_pk")
        )
        if not conv_id:
            return Response({"detail": "conversation_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conv = Conversation.objects.get(conversation_id=conv_id)
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
    ordering_fields = ["-created_at"]
    search_fields = ["participants__username"]
    filterset_class = MessageFilter
