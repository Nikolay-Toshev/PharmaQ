from django.shortcuts import render
from django.views.generic import CreateView

from PharmaQ.message.forms import MessageCreateForm
from PharmaQ.message.models import Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'messages/message-create.html'



    def get_success_url(self):
        pass
