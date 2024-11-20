from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView


class AppIndexView(TemplateView):
    template_name = 'common/index.html'


def send_test_email(request):
    subject = 'Тестов имейл'
    message = 'Това е тестово съобщение от Django проект с Mailjet.'
    recipient_list = [request.user.email]

    try:
        send_mail(subject, message, None, recipient_list)
        return HttpResponse("Имейлът беше изпратен успешно!")
    except Exception as e:
        return HttpResponse(f"Грешка при изпращане на имейла: {e}")