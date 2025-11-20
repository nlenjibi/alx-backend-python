from django_filters import rest_framework as filters
from django.apps import apps


class MessageFilter(filters.FilterSet):
    """FilterSet for Message model to filter by conversation, sender, recipient and time range."""

    conversation = filters.NumberFilter(field_name="conversation__id")
    sender = filters.NumberFilter(field_name="sender__id")
    recipient = filters.NumberFilter(method="filter_recipient")
    start_time = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_time = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    def filter_recipient(self, queryset, name, value):
        # Try common recipient-related fields
        qs = queryset
        try:
            qs = qs.filter(recipient__id=value)
        except Exception:
            try:
                qs = qs.filter(participants__id=value)
            except Exception:
                pass
        return qs

    class Meta:
        # Expect a `Message` model in `messaging_app.chats.models`
        Message = apps.get_model("messaging_app.chats", "Message")
        model = Message
        fields = ["conversation", "sender", "recipient", "start_time", "end_time"]
