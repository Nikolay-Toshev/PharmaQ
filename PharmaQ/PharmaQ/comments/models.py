from django.contrib.auth import get_user_model
from django.db import models

from PharmaQ.consultation.models import Answer

UserModel = get_user_model()

class Comment(models.Model):

    content = models.CharField(max_length=500)

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    class Meta:

        ordering = ['-created_at']
