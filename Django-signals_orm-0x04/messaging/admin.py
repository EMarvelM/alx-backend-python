from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model."""
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'read')
    list_filter = ('edited', 'read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    raw_id_fields = ('sender', 'receiver', 'parent_message')
    readonly_fields = ('timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    list_display = ('id', 'user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username',)
    raw_id_fields = ('user', 'message')
    readonly_fields = ('created_at',)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """Admin interface for MessageHistory model."""
    list_display = ('id', 'message', 'old_content', 'edited_at', 'edited_by')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content')
    raw_id_fields = ('message', 'edited_by')
    readonly_fields = ('edited_at',)
