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


    def form_valid(self, form):

        question = form.save(commit=False)
        question.creator_id = self.request.user

        response = super().form_valid(form)

        return response


    def test_func(self):
        return self.request.user.groups.filter(name__exact='patient').exists()


    def get_success_url(self):
        return reverse_lazy('question-list', kwargs={'user_pk': self.request.user.pk})


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
        return reverse_lazy('question-list', kwargs={'user_pk': self.kwargs['user_pk']})

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
        return reverse_lazy('question-list', kwargs={'user_pk': self.request.user.pk})

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

