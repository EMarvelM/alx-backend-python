from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Message, Notification, MessageHistory


@login_required
def delete_user(request):
    """
    View that allows a user to delete their account.
    The post_delete signal on User model will handle cleanup of related data.
    """
    if request.method == 'POST':
        user = request.user
        # Log out the user first
        from django.contrib.auth import logout
        logout(request)
        # Delete the user (this triggers the post_delete signal)
        user.delete()
        django_messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    
    return render(request, 'messaging/delete_user.html')


@cache_page(60)
@login_required
def inbox(request):
    """
    Display unread messages for the logged-in user.
    Uses Message.objects.filter with .only() optimization.
    Cached for 60 seconds.
    """
    unread_messages = Message.objects.filter(
        receiver=request.user,
        read=False
    ).select_related(
        'sender', 'receiver'
    ).only(
        'id', 'sender', 'content', 'timestamp', 'parent_message'
    )
    return render(request, 'messaging/inbox.html', {'messages': unread_messages})


@login_required
def message_thread(request, message_id):
    """
    Display a message thread with all replies.
    Uses select_related and prefetch_related for optimization.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message'),
        pk=message_id
    )
    
    # Get all replies using prefetch_related for optimization
    replies = message.get_thread()
    
    return render(request, 'messaging/thread.html', {
        'message': message,
        'replies': replies
    })


@login_required
def conversation_thread(request, message_id):
    """
    Display a full conversation thread starting from a specific message.
    Uses advanced ORM techniques for efficient querying.
    """
    thread = Message.get_conversation_thread(message_id)
    return render(request, 'messaging/conversation.html', {'thread': thread})


@login_required
def message_history(request, message_id):
    """
    Display the edit history of a message.
    Allows users to view previous versions of their messages.
    """
    message = get_object_or_404(Message, pk=message_id)
    history = MessageHistory.objects.filter(message=message).select_related('edited_by')
    
    return render(request, 'messaging/history.html', {
        'message': message,
        'history': history
    })


@login_required
def notifications(request):
    """
    Display notifications for the logged-in user.
    """
    user_notifications = Notification.objects.filter(
        user=request.user
    ).select_related('message', 'message__sender')
    
    return render(request, 'messaging/notifications.html', {
        'notifications': user_notifications
    })


@login_required
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read.
    """
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('notifications')


@login_required
def send_message(request):
    """
    Send a new message to another user.
    """
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_message')
        
        receiver = get_object_or_404(User, pk=receiver_id)
        
        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, pk=parent_id)
        
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        
        django_messages.success(request, 'Message sent successfully!')
        return redirect('inbox')
    
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'messaging/send_message.html', {'users': users})


@login_required
def edit_message(request, message_id):
    """
    Edit an existing message.
    The pre_save signal will log the old content to MessageHistory.
    """
    message = get_object_or_404(Message, pk=message_id, sender=request.user)
    
    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content and new_content != message.content:
            message.content = new_content
            message.save()  # This triggers the pre_save signal
            django_messages.success(request, 'Message updated successfully!')
        return redirect('message_thread', message_id=message_id)
    
    return render(request, 'messaging/edit_message.html', {'message': message})
