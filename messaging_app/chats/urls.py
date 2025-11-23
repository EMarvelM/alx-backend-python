from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from .auth import RegisterView

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
