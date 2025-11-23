from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class MessagingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='password123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='password123',
            first_name='User',
            last_name='Two'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body='Hello!'
        )

    def test_conversation_creation(self):
        self.assertEqual(self.conversation.participants.count(), 2)

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.user1)
        self.assertEqual(self.message.conversation, self.conversation)