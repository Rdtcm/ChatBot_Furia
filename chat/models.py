# flake8: noqa
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_conversations')
    start_time = models.DateTimeField(auto_now_add=True)
    last_interaction_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversa com Bot (Usuario: {self.user.username}, ID: {self.id})"


class Messages(models.Model):
    ...