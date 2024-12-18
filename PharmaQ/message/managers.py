from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class MessageManager(models.Manager):

    def filter_by_sender(self, sender_id):
        return self.filter(sender__id=sender_id)

    def filter_by_receiver(self, receiver_id):
        return self.filter(receiver__id=receiver_id)

