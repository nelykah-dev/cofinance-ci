from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation

@login_required
def chat_page(request):
    user = request.user
    conversations = []
    active_conversation = None
    active_id = request.GET.get('conversation_id')
    
    if user.role == 'client':
        # Le client voit uniquement sa propre conversation
        active_conversation = Conversation.objects.filter(client=user).first()
        if not active_conversation:
            active_conversation = Conversation.objects.create(client=user)
        if active_conversation:
            conversations = [active_conversation]
            active_id = active_conversation.id
    
    else:
        # Agent ou Admin : voit toutes les conversations
        conversations = Conversation.objects.all().order_by('-id')
        if active_id:
            try:
                active_conversation = Conversation.objects.get(id=active_id)
            except Conversation.DoesNotExist:
                active_conversation = conversations.first() if conversations else None
        else:
            active_conversation = conversations.first() if conversations else None
    
    context = {
        'user': user,
        'conversations': conversations,
        'active_conversation': active_conversation,
        'active_conversation_id': active_conversation.id if active_conversation else None,
        'username': user.username,
        'role': user.role,
    }
    return render(request, 'chat/index.html', context)