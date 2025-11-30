from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('delete-account/', views.delete_user, name='delete_user'),
    path('message/<int:message_id>/', views.message_thread, name='message_thread'),
    path('conversation/<int:message_id>/', views.conversation_thread, name='conversation_thread'),
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('send/', views.send_message, name='send_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]
