from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_patient:
            subject = 'Welcome to PharmaQ!'
            message = f'Hello {instance.username}. Wellcome to PharmaQ!'
            recipient_list = [instance.email]
            send_mail(subject, message, None, recipient_list)
        if instance.is_pharmacist:
            subject = 'Verifying Pharmacist'
            message = f'Hello {instance.username}! Your pharmacist credentials are \
            being verified. You will receive an email when you are verified.'
            recipient_list = [instance.email]
            send_mail(subject, message, None, recipient_list)
            moderators = UserModel.objects.filter(groups__name='site-moderator').all()
            for moderator in moderators:
                send_mail('New Pharmacist', 'There is new pharmacist for approval', None, [moderator.email])

@receiver(pre_save, sender=UserModel)
def approve_pharmacist(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = UserModel.objects.get(pk=instance.pk)
        except UserModel.DoesNotExist:
            previous_instance = None

        if previous_instance:
            if previous_instance.is_active != instance.is_active:
                if not previous_instance.is_active and instance.is_active:
                    subject = 'Welcome to PharmaQ!'
                    message = f'Hello {instance.username}. Wellcome to PharmaQ!'
                    recipient_list = [instance.email]
                    send_mail(subject, message, None, recipient_list)