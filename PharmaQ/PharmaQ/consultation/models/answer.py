from django.contrib.auth import get_user_model
from django.db import models
from PharmaQ.consultation.models.question import Question

UserModel = get_user_model()

class Answer(models.Model):

    content = models.CharField(max_length=200)

    question_id = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    creator_id = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)