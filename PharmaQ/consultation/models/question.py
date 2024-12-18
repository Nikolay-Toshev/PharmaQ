from django.contrib.auth import get_user_model
from django.db import models
from PharmaQ.consultation.managers import QuestionManager
from PharmaQ.consultation.models.category import Category

UserModel = get_user_model()

class Question(models.Model):

    title = models.CharField(max_length=50)

    content = models.CharField(max_length=200)

    category_id = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='questions',
    )

    creator_id = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Въпрос: {self.title} зададен от: {self.creator_id}'

    class Meta:
        ordering = ['created_at']


    objects = QuestionManager()