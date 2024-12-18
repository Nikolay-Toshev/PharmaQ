from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ForeignKey
from PharmaQ.consultation.models import Answer

UserModel = get_user_model()

class Rating(models.Model):

    like = models.BooleanField(default=False)

    dislike = models.BooleanField(default=False)

    patient_id = ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='ratings',
    )

    answer_id = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='ratings',
    )

    class Meta:
        unique_together = (('patient_id', 'answer_id'),)

