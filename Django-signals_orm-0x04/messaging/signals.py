from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a new message is created.
    Triggers only when a new message is created, not on updates.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log the old content of a message before it's updated.
    Creates a MessageHistory entry with the old content.
    """
    if instance.pk:  # Only for existing messages (updates)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content has changed
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                # Mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass  # New message, no history to log


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all user-related data when a user is deleted.
    Deletes all messages, notifications, and message histories associated with the user.
    
    Note: Due to CASCADE on foreign keys, most related objects will be automatically
    deleted. This signal handles any additional cleanup if needed.
    """
    # Messages where user is sender or receiver are automatically deleted via CASCADE
    # Notifications linked to user are automatically deleted via CASCADE
    # MessageHistory entries linked to messages are automatically deleted via CASCADE
    
    # Additional cleanup for any orphaned data if needed
    # This is mostly handled by CASCADE, but we can add custom logic here
    pass
