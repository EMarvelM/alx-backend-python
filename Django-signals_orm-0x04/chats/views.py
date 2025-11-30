from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from messaging.models import Message


@cache_page(60)  # Cache for 60 seconds
def conversation_messages(request, conversation_id):
    """
    View to display a list of messages in a conversation.
    Cached for 60 seconds to improve performance.
    
    Uses select_related and prefetch_related for optimized querying.
    """
    messages = Message.objects.filter(
        id=conversation_id
    ).select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related(
        'replies__sender',
        'replies__receiver'
    )
    
    return render(request, 'chats/conversation.html', {
        'messages': messages
    })


@cache_page(60)  # Cache for 60 seconds
@login_required
def message_list(request):
    """
    View to display all messages for the current user.
    Cached for 60 seconds to reduce database load.
    """
    messages = Message.objects.filter(
        receiver=request.user
    ).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        'replies'
    ).order_by('-timestamp')
    
    return render(request, 'chats/message_list.html', {
        'messages': messages
    })
