from django.db import models
from accounts.models import User

class Conversation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_client')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations_agent')
    date_creation = models.DateTimeField(auto_now_add=True)
    est_fermee = models.BooleanField(default=False)

    def __str__(self):
        return f"Conversation {self.id} - {self.client.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_envoi']

    def __str__(self):
        return f"Message de {self.expediteur.username} - {self.date_envoi}"