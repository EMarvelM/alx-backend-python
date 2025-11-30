from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    """
    Message model for storing messages between users.
    Includes support for threaded conversations via parent_message.
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Default manager
    objects = models.Manager()
    # Custom manager for unread messages
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_thread(self):
        """
        Get all replies to this message recursively using prefetch_related.
        Returns a queryset of all messages in the thread.
        """
        return Message.objects.filter(
            parent_message=self
        ).select_related('sender', 'receiver').prefetch_related('replies')

    @classmethod
    def get_conversation_thread(cls, message_id):
        """
        Get a full conversation thread starting from a specific message.
        Uses select_related and prefetch_related for optimization.
        """
        return cls.objects.filter(
            models.Q(id=message_id) | models.Q(parent_message_id=message_id)
        ).select_related(
            'sender', 'receiver', 'parent_message'
        ).prefetch_related(
            'replies__sender',
            'replies__receiver',
            'replies__replies'
        )


class Notification(models.Model):
    """
    Notification model to store notifications for users.
    Linked to User and Message models.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user} - Message from {self.message.sender}"


class MessageHistory(models.Model):
    """
    MessageHistory model to log message edits.
    Stores the old content before a message is edited.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_edits'
    )

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Message Histories'

    def __str__(self):
        return f"Edit history for Message {self.message.id} at {self.edited_at}"
