from django.contrib.auth.models import AbstractUser
from django.db import models

from PharmaQ.accounts.validators import ImageSizeValidator


class AppUser(AbstractUser):

    email = models.EmailField(unique=True)

    personal_info = models.TextField(blank=True, null=True)

    profile_img = models.ImageField(upload_to="profile_imgs/", blank=True, null=True, validators=[ImageSizeValidator(5)])

    is_patient = models.BooleanField(default=False)

    is_pharmacist = models.BooleanField(default=False)

    is_approved = models.BooleanField(default=True)

    professional_card = models.ImageField(upload_to="professional_cards/", blank=True, null=True, validators=[ImageSizeValidator(5)])

    def save(self, *args, **kwargs):
        if self.pk:
            old_profile_img = AppUser.objects.get(pk=self.pk).profile_img
            if old_profile_img and old_profile_img != self.profile_img:
                old_profile_img.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username