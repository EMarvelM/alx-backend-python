import django_filters
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'timestamp_after', 'timestamp_before']

class ConversationFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='participants__username', lookup_expr='icontains')

    class Meta:
        model = Conversation
        fields = ['participant']