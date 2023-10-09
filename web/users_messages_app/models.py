import uuid

from django.db import models
from uuid import uuid4
from django.db.models import (SlugField, CharField, TextField, DateTimeField, ForeignKey, ManyToManyField, BooleanField)
from django.utils import timezone
from authapp.models import CustomUser

# Create your models here.
class Chat(models.Model):

    '''
    Модель чатов юзера
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(max_length=255, verbose_name='Название')
    created_at = DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='url', db_index=True)

    users = ManyToManyField(CustomUser, related_name='chats')

    def __str__(self):
        users = self.users.all()
        result = "::".join([user.username for user in users])
        return result

class ChatMessage(models.Model):
    '''
    Модель сообщений юзера
    author - модель юзера создавшего сообщений
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = TextField()
    created_at = DateTimeField(default=timezone.now)
    new = BooleanField(default=True)

    ##
    author = ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False, related_name='message')
    chat = ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return str(self.author) + str(self.chat) + 'text: ' + str(self.text)
