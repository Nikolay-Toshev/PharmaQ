from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from PharmaQ.consultation.forms import AnswerCreateForm
from PharmaQ.consultation.models import Answer, Question, question


UserModel = get_user_model()

class AnswerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'consultations/answer/answer-create.html'
    form_class = AnswerCreateForm
    success_url = reverse_lazy('index') #to be fixed

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        question = Question.objects.get(pk=self.kwargs['pk'])
        context['question'] = question
        return context

    def test_func(self):
        return self.request.user.groups.filter(name__exact='pharmacist').exists()

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        answer = form.save(commit=False)
        answer.creator_id = self.request.user
        answer.question_id = question

        response = super().form_valid(form)

        return response


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    pass


class AnswerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Answer
    template_name = 'consultations/answer/answer-list.html'
    context_object_name = 'answers'

    def get_queryset(self):
        return Answer.objects.filter_by_creator(creator_id=self.request.user.pk)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

