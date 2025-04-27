# flake8: noqa
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
Cada conversa esta diretamente ligada a um usuario

ESTRUTURA:

Um usuário ➔ pode ter várias conversas.

Uma conversa ➔ pode ter várias mensagens.

Uma mensagem ➔ pertence a uma única conversa.

'''


class Conversation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bot_conversations'
    )
    start_time = models.DateTimeField(
        auto_now_add=True
    )
    last_interaction_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Conversa com Bot (Usuario: {self.user.username}, ID: {self.id})"


class Messages(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_bot_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_bot = models.BooleanField(default=False)

    def __str__(self):
        sender_str = "Bot" if self.is_bot else self.sender.username
        return f"Mensagem de {sender_str} em {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
