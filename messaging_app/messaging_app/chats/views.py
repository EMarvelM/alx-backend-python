from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation

class ConversationListView(APIView):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get(self, request):
        # For now, just return a test response
        return Response({"message": "ConversationListView works!"})


class MessageListView(APIView):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get(self, request):
        return Response({"message": "MessageListView works!"})
