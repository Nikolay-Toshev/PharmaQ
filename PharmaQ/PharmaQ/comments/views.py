from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from PharmaQ.comments.forms import CommentEditForm
from PharmaQ.comments.models import Comment
from PharmaQ.consultation.models import Answer, Question

UserModel = get_user_model()

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = 'comments/comment-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer = Answer.objects.get(pk=self.object.answer_id)
        question = Question.objects.get(pk=answer.question_id_id)
        context['answer'] = answer
        context['question'] = question

        return context

    def test_func(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        author = UserModel.objects.get(pk=comment.author_id)
        return self.request.user == author

    def get_success_url(self):

        if self.request.user.groups.filter(name__exact='patient').exists():
            answer = Answer.objects.get(pk=self.object.answer_id)
            question = Question.objects.get(pk=answer.question_id_id)
            return reverse_lazy('my-question-details', kwargs={'user_pk': self.request.user.pk, 'question_pk': question.pk})
        if self.request.user.groups.filter(name__exact='pharmacist').exists():
            answer = Answer.objects.get(pk=self.object.answer_id)
            return reverse_lazy('my-answer-details', kwargs={'user_pk': self.request.user.pk, 'answer_pk': answer.pk })

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment-delete.html'

    def test_func(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        author = UserModel.objects.get(pk=comment.author_id)
        return self.request.user == author

    def get_success_url(self):
        if self.request.user.groups.filter(name__exact='patient').exists():
            answer = Answer.objects.get(pk=self.object.answer_id)
            question = Question.objects.get(pk=answer.question_id_id)
            return reverse_lazy('my-question-details', kwargs={'user_pk': self.request.user.pk, 'question_pk': question.pk})
        if self.request.user.groups.filter(name__exact='pharmacist').exists():
            answer = Answer.objects.get(pk=self.object.answer_id)
            return reverse_lazy('my-answer-details', kwargs={'user_pk': self.request.user.pk, 'answer_pk': answer.pk })
