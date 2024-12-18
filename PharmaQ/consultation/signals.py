from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from PharmaQ.consultation.models import Answer


@receiver(post_save, sender=Answer)
def send_email_notification(sender, instance, created, **kwargs):
    if created:
        question = instance.question_id
        email_receiver = question.creator_id
        subject = 'Нов отговор'
        message = f'На вашият въпрос "{question.title}" беше отговорено. можете да влезнете в профила си и да го прочетете.'
        recipient_list = [email_receiver.email]
        send_mail(subject, message, None, recipient_list)