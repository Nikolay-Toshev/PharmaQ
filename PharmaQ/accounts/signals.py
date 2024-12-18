from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_patient:
            subject = 'Добре дошли във PharmaQ!'
            message = (f'Здравейте, {instance.username}! Благодарим Ви, че се регистрирахте в във PharmaQ! Радваме се, че сте с нас.'
                       f' Ако имате въпроси или се нуждаете от помощ, не се колебайте да се свържете с нас на support@pharma-q.org')
            recipient_list = [instance.email]
            send_mail(subject, message, None, recipient_list)
        if instance.is_pharmacist:
            subject = 'Потвърждение за проверка на Вашата регистрация'
            message = (f'Здравейте, {instance.username}! Вашата регистрация като фармацевт е в процес на проверка. '
                       f'Ще Ви изпратим имейл, когато тя бъде успешно потвърдена.')
            recipient_list = [instance.email]
            send_mail(subject, message, None, recipient_list)
            moderators = UserModel.objects.filter(groups__name='site-moderator').all()
            for moderator in moderators:
                send_mail('Нов фармацевт', 'Нов фармацевт очаква одобрение', None, [moderator.email])

@receiver(pre_save, sender=UserModel)
def approve_pharmacist(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = UserModel.objects.get(pk=instance.pk)
        except UserModel.DoesNotExist:
            previous_instance = None

        if previous_instance:
            if previous_instance.is_approved != instance.is_approved:
                if not previous_instance.is_approved and instance.is_approved:
                    subject = 'Добре дошли във PharmaQ!'
                    message = (f'Здравейте, {instance.username}! Благодарим Ви, че се регистрирахте в във PharmaQ! Радваме се, че сте с нас.'
                       f' Ако имате въпроси или се нуждаете от помощ, не се колебайте да се свържете с нас на support@pharma-q.org')
                    recipient_list = [instance.email]
                    send_mail(subject, message, None, recipient_list)