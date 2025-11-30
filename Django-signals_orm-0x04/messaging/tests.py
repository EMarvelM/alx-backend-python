from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message, Notification, MessageHistory


class MessageModelTest(TestCase):
    """Test cases for Message model."""

    def setUp(self):
        """Set up test users."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )

    def test_message_creation(self):
        """Test that a message can be created."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, User2!'
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Hello, User2!')
        self.assertFalse(message.edited)
        self.assertFalse(message.read)

    def test_threaded_message(self):
        """Test that messages can be threaded."""
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original message'
        )
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent
        )
        self.assertEqual(reply.parent_message, parent)
        self.assertIn(reply, parent.replies.all())


class NotificationSignalTest(TestCase):
    """Test cases for notification signal."""

    def setUp(self):
        """Set up test users."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )

    def test_notification_created_on_new_message(self):
        """Test that notification is created when a new message is sent."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, User2!'
        )
        notification = Notification.objects.filter(
            user=self.user2,
            message=message
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user2)
        self.assertFalse(notification.is_read)


class MessageHistorySignalTest(TestCase):
    """Test cases for message history signal."""

    def setUp(self):
        """Set up test users and message."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )

    def test_message_history_on_edit(self):
        """Test that message history is created when a message is edited."""
        old_content = self.message.content
        self.message.content = 'Edited content'
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, old_content)
        
        # Refresh from database
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)


class UserDeletionTest(TestCase):
    """Test cases for user deletion and cleanup."""

    def setUp(self):
        """Set up test users and data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        # Create messages
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )

    def test_messages_deleted_on_user_deletion(self):
        """Test that messages are deleted when user is deleted."""
        message_id = self.message.id
        self.user1.delete()
        
        # Check that the message was deleted (CASCADE)
        self.assertFalse(Message.objects.filter(id=message_id).exists())


class UnreadMessagesManagerTest(TestCase):
    """Test cases for UnreadMessagesManager."""

    def setUp(self):
        """Set up test users and messages."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        # Create unread messages
        self.unread_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Unread message',
            read=False
        )
        # Create read message
        self.read_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Read message',
            read=True
        )

    def test_unread_for_user(self):
        """Test that unread_for_user returns only unread messages."""
        unread = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread.count(), 1)
        self.assertIn(self.unread_message, unread)
        self.assertNotIn(self.read_message, unread)

    def test_unread_manager_default_queryset(self):
        """Test that UnreadMessagesManager filters unread by default."""
        all_unread = Message.unread.all()
        self.assertEqual(all_unread.count(), 1)
