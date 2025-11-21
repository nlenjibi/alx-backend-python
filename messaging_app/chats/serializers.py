from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # expose username, email and role minimally
        fields = ("user_id", "username", "first_name", "last_name", "email", "phone_number", "role")


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # expose the message body as a CharField alias `content`
    content = serializers.CharField(source="message_body")

    class Meta:
        model = Message
        fields = ("message_id", "sender", "conversation", "content", "sent_at")
        read_only_fields = ("message_id", "sent_at", "sender")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)
    # include a computed field for the number of messages
    messages_count = serializers.SerializerMethodField()
    # optional title field for conversation creation
    title = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Conversation
        fields = ("conversation_id", "participants", "created_at", "messages")
        read_only_fields = ("conversation_id", "created_at", "messages")

    def get_messages_count(self, obj):
        return obj.messages.count()

    def create(self, validated_data):
        participants_data = validated_data.pop("participants", [])
        if not participants_data:
            raise serializers.ValidationError("participants list is required")

        conv = Conversation.objects.create(**validated_data)
        for p in participants_data:
            # participants provided as nested objects; try to add by user_id or username
            user = None
            if "user_id" in p:
                try:
                    user = User.objects.get(user_id=p["user_id"])
                except User.DoesNotExist:
                    user = None
            if not user and "username" in p:
                try:
                    user = User.objects.get(username=p["username"])
                except User.DoesNotExist:
                    user = None
            if not user:
                raise serializers.ValidationError(f"Participant not found: {p}")
            conv.participants.add(user)
        return conv
