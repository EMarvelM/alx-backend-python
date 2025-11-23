from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # obj could be a Conversation or Message instance
        return request.user in obj.participants.all()
