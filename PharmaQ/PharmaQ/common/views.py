from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
from mailjet_rest import Client

from PharmaQ import settings


class AppIndexView(TemplateView):
    template_name = 'common/index.html'


def send_test_email(request): #  for email testing
    subject = 'Wellcome to PharmaQ'
    message = 'Това е тестово съобщение от Django проект с Mailjet.'
    recipient_list = [request.user.email]

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
        return HttpResponse("Имейлът беше изпратен успешно!")
    except Exception as e:
        return HttpResponse(f"Грешка при изпращане на имейла: {e}")



