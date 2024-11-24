from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()
class Message(models.Model):

    content = models.CharField(max_length=200)

    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', 'is_read']