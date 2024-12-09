
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from PharmaQ.common.mixins import SearchMixin
from PharmaQ.message.forms import MessageCreateForm
from PharmaQ.message.models import Message

UserModel =get_user_model()

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'messages/message-create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        message = form.save(commit=False)
        sender = self.request.user
        receiver = get_object_or_404(UserModel, pk=self.kwargs['receiver_pk'])
        message.sender = sender
        message.receiver = receiver
        message.save()

        response = super().form_valid(form)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver = get_object_or_404(UserModel, pk=self.kwargs['receiver_pk'])
        context["receiver"] = receiver
        return context

class SentMessageListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Message
    context_object_name = 'all_messages'
    template_name = 'messages/message-sent-list.html'
    paginate_by = 5

    search_fields = ['receiver__username', 'content'] #what should be filtering???

    def get_queryset(self):
        queryset = Message.objects.filter(sender=self.request.user)
        queryset = self.apply_search_filter(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ReceivedMessageListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Message
    context_object_name = 'all_messages'
    template_name = 'messages/message-received-list.html'
    paginate_by = 5

    search_fields = ['receiver__username', 'content']

    def get_queryset(self):
        queryset = Message.objects.filter(receiver=self.request.user)
        queryset = self.apply_search_filter(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    context_object_name = 'message'
    template_name = 'messages/message-details.html'


    def get_object(self, queryset=None):
        message = get_object_or_404(Message, pk=self.kwargs['message_pk'])
        user = get_object_or_404(UserModel, pk=self.request.user.pk)
        if user == message.receiver:
            message.is_read = True
            message.save()

        return message

    def test_func(self):
        message = get_object_or_404(Message, pk=self.kwargs['message_pk'])
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return user == message.receiver or message.sender == user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'messages/message-delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        message_pk = self.kwargs['message_pk']
        return Message.objects.get(pk=message_pk)



    def test_func(self):
        message = get_object_or_404(Message, pk=self.kwargs['message_pk'])
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return user == message.receiver or message.sender == user


class ContactUsMessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'messages/contact-us.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return user == self.request.user

    def form_valid(self, form):
        message = form.save(commit=False)
        sender = self.request.user
        receiver = UserModel.objects.filter(groups__name='site-moderator').first()
        message.sender = sender
        message.receiver = receiver
        message.save()

        response = super().form_valid(form)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver = UserModel.objects.filter(groups__name='site-moderator').first()
        context["receiver"] = receiver
        return context