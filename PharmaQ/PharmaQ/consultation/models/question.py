from django.contrib.auth import get_user_model
from django.db import models
from PharmaQ.consultation.models.category import Category

UserModel = get_user_model()

class Question(models.Model):

    title = models.CharField(max_length=50)

    content = models.CharField(max_length=200)

    category_id = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    creator_id = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
