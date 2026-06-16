import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from accounts.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        contenu = data.get('message', '')
        user_id = data.get('user_id')
        if not contenu or not user_id:
            return
        message = await self.sauvegarder_message(user_id, contenu)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': contenu,
                'expediteur': message['expediteur'],
                'date_envoi': message['date_envoi'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'expediteur': event['expediteur'],
            'date_envoi': event['date_envoi'],
        }))

    @database_sync_to_async
    def sauvegarder_message(self, user_id, contenu):
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            expediteur=user,
            contenu=contenu,
        )
        return {
            'expediteur': user.username,
            'date_envoi': str(message.date_envoi),
        }