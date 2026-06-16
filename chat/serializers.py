from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    expediteur = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['expediteur', 'date_envoi', 'conversation']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField(read_only=True)
    agent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['client', 'date_creation']