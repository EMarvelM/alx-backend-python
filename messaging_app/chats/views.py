from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter, ConversationFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filterset_class = ConversationFilter

    def get_queryset(self):
        return self.request.user.conversations.all()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if not conversation or self.request.user not in conversation.participants.all():
            from rest_framework import status
            from rest_framework.response import Response
            raise Response({'error': 'You are not a participant in this conversation'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)
