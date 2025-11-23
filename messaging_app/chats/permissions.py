from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Only allow authenticated participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj could be a Conversation or Message instance
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # For updates and deletes, ensure user is participant
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            elif hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
        # For GET and other methods, allow participants to view
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
