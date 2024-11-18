from PIL.SpiderImagePlugin import iforms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from PharmaQ.accounts.models import AppUser
from PharmaQ.consultation.forms import QuestionCreateForm, QuestionEditForm
from PharmaQ.consultation.models import Question, Answer

UserModel = get_user_model()

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'consultations/question/question-create.html'


    def form_valid(self, form):

        question = form.save(commit=False)
        question.creator_id = self.request.user

        response = super().form_valid(form)

        return response


    def test_func(self):
        return self.request.user.groups.filter(name__exact='patient').exists()


    def get_success_url(self):
        return reverse_lazy('my-question-list', kwargs={'user_pk': self.request.user.pk})


class QuestionEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionEditForm
    template_name = 'consultations/question/question-edit.html'
    # success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('user_pk')
        question_pk = self.kwargs.get('question_pk')
        return get_object_or_404(Question, pk=question_pk, creator_id=user_pk)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy('my-question-list', kwargs={'user_pk': self.kwargs['user_pk']})

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'consultations/question/question-delete.html'

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('user_pk')
        question_pk = self.kwargs.get('question_pk')
        return get_object_or_404(Question, pk=question_pk, creator_id=user_pk)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.request.user.id)
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy('my-question-list', kwargs={'user_pk': self.request.user.pk})

class MyQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Question
    template_name = 'consultations/question/question-list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(creator_id=self.request.user.id)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return self.request.user == user


class UnansweredQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Question
    template_name = 'consultations/question/question-list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(answers__isnull=True)

    def test_func(self):
        return self.request.user.groups.filter(name__exact='pharmacist').exists()


class MyQuestionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'consultations/question/question-details.html'

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('user_pk')
        question_pk = self.kwargs.get('question_pk')
        return get_object_or_404(Question, pk=question_pk, creator_id_id=user_pk)


    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(AppUser, pk=self.kwargs['user_pk'])
        try:
            answer = get_object_or_404(Answer, question_id_id=self.kwargs['question_pk'])
            pharmacist = get_object_or_404(AppUser, pk=answer.creator_id_id)
            context['answer'] = answer
            context['pharmacist'] = pharmacist
        except Http404:
            pass

        context['patient'] = patient

        return context

