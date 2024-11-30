from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):

    personal_info = models.TextField(blank=True, null=True)

    profile_img = models.ImageField(upload_to="profile_imgs/", blank=True, null=True)

    is_patient = models.BooleanField(default=False)

    is_pharmacist = models.BooleanField(default=False)

    professional_card = models.ImageField(upload_to="professional_cards/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_profile_img = AppUser.objects.get(pk=self.pk).profile_img
            if old_profile_img and old_profile_img != self.profile_img:
                old_profile_img.delete(save=False)
        super().save(*args, **kwargs)
