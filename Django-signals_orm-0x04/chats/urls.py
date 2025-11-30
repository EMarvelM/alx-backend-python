from django.urls import path
from . import views

urlpatterns = [
    path('conversation/<int:conversation_id>/', views.conversation_messages, name='conversation_messages'),
    path('messages/', views.message_list, name='message_list'),
]
