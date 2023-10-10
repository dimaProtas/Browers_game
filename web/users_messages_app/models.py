from django.db import models
from django.utils import timezone
from authapp.models import CustomUser


class PrivateMessagesModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_message')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient_message')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'recipient'], name='sender_recipient_idx')
        ]
        ordering = ['-timestamp']
        verbose_name = 'Личные сообщения'
