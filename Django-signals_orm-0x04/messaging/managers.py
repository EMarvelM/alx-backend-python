from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    Uses .only() to retrieve only necessary fields for optimization.
    """

    def get_queryset(self):
        """Override get_queryset to return unread messages by default."""
        return super().get_queryset().filter(read=False)

    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user.
        Optimized with .only() to fetch only necessary fields.
        """
        return self.get_queryset().filter(
            receiver=user
        ).only('id', 'sender', 'content', 'timestamp', 'parent_message')

    def for_user(self, user):
        """
        Returns all unread messages for a specific user.
        """
        return self.get_queryset().filter(receiver=user)
