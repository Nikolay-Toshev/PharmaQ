from django.contrib.auth import get_user_model
from django.db import models

from PharmaQ.message.managers import MessageManager

UserModel = get_user_model()

class Message(models.Model):

    content = models.CharField(max_length=200)

    sender = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )

    receiver = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='received_messages',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_read', '-created_at']

    objects = MessageManager()