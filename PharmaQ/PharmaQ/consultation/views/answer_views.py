from unicodedata import category

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from PharmaQ.consultation.forms import AnswerCreateForm, AnswerEditForm
from PharmaQ.consultation.models import Answer, Question, Category

UserModel = get_user_model()

class AnswerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'consultations/answer/answer-create.html'
    form_class = AnswerCreateForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        question = Question.objects.get(pk=self.kwargs['question_pk'])
        context['question'] = question
        return context

    def test_func(self):
        return self.request.user.groups.filter(name__exact='pharmacist').exists()

    def dispatch(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'])

        if Answer.objects.filter(question_id=question).exists():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'])
        answer = form.save(commit=False)
        answer.creator_id = self.request.user
        answer.question_id = question

        response = super().form_valid(form)

        return response

    def get_success_url(self):
        user = get_object_or_404(UserModel, pk=self.request.user.pk)
        return reverse_lazy('unanswered-question-list', kwargs={'user_pk': user.pk})


class AnswerEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    template_name = 'consultations/answer/answer-edit.html'
    form_class = AnswerEditForm

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        answer_pk = self.kwargs['answer_pk']
        return get_object_or_404(Answer, pk=answer_pk, creator_id=user_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer_to_edit = get_object_or_404(Answer, pk=self.kwargs['answer_pk'])
        question = get_object_or_404(Question, pk=answer_to_edit.question_id_id)
        context['question'] = question
        return context

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.request.user.pk)
        answer_to_edit = get_object_or_404(Answer, pk=self.kwargs['answer_pk'])
        return user == answer_to_edit.creator_id

    def get_success_url(self):
        return reverse_lazy('answer-list', kwargs={'user_pk': self.request.user.pk})

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'consultations/answer/answer-delete.html'

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        answer_pk = self.kwargs['answer_pk']
        return get_object_or_404(Answer, pk=answer_pk, creator_id=user_pk)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.request.user.pk)
        return user == self.request.user

    def get_success_url(self):
        return reverse_lazy('answer-list', kwargs={'user_pk': self.request.user.pk})


class AnswerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Answer
    template_name = 'consultations/answer/answer-list.html'
    context_object_name = 'answers'

    search_fields = ['content', 'question_id__title']


    def get_queryset(self):
        queryset = Answer.objects.filter_by_creator(creator_id=self.request.user.pk)
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if query and self.search_fields:
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(search_query)

        if category_id:
            queryset = queryset.filter(question_id__category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return self.request.user == user


class MyAnswerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Answer
    context_object_name = 'answer'
    template_name = 'consultations/answer/answer-details.html'

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        answer_pk = self.kwargs['answer_pk']
        return get_object_or_404(Answer, pk=answer_pk, creator_id=user_pk)

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pharmacist = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        question = get_object_or_404(Question, answers=self.kwargs['answer_pk'])
        patient = get_object_or_404(UserModel, pk=question.creator_id_id)

        context['pharmacist'] = pharmacist
        context['question'] = question
        context['patient'] = patient

        return context

