from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from PharmaQ.consultation.forms import QuestionCreateForm, QuestionEditForm
from PharmaQ.consultation.models import Question


UserModel = get_user_model()

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'consultations/question/question-create.html'
    success_url = reverse_lazy('index') # to be changed to dashboard

    def form_valid(self, form):

        question = form.save(commit=False)
        question.creator_id = self.request.user

        response = super().form_valid(form)

        return response


    def test_func(self):
        return self.request.user.groups.filter(name__exact='patient').exists()


class QuestionEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionEditForm
    template_name = 'consultations/question/question-edit.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='patient').exists()


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'consultations/question/question-delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='patient').exists()


class MyQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Question
    template_name = 'consultations/question/question-list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(creator_id=self.request.user.id)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user


class UnansweredQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Question
    template_name = 'consultations/question/question-list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(answers__isnull=True)

    def test_func(self):
        return self.request.user.groups.filter(name__exact='pharmacist').exists()

