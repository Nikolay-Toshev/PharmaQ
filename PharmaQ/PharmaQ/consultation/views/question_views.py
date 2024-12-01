from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from PharmaQ.comments.forms import CommentCreateForm
from PharmaQ.comments.models import Comment
from PharmaQ.common.mixins import SearchMixin
from PharmaQ.consultation.forms import QuestionCreateForm, QuestionEditForm
from PharmaQ.consultation.models import Question, Answer, Category
from PharmaQ.rating.forms import LikeForm, DislikeForm
from PharmaQ.rating.models import Rating

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
        return reverse_lazy('my-question-details', kwargs={'user_pk': self.kwargs['user_pk'], 'question_pk': self.kwargs['question_pk']})

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

class MyQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, SearchMixin, ListView):
    model = Question
    template_name = 'consultations/question/question-list.html'
    context_object_name = 'questions'
    paginate_by = 10

    search_fields = ['title', 'content']

    def get_queryset(self):
        queryset = Question.objects.filter(creator_id=self.request.user.id)
        queryset = self.apply_search_filter(queryset)

        return queryset

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        context['user'] = user
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class UnansweredQuestionsListView(LoginRequiredMixin, UserPassesTestMixin, SearchMixin, ListView):
    model = Question
    template_name = 'consultations/question/question-list.html'
    context_object_name = 'questions'
    paginate_by = 10

    search_fields = ['title', 'content']

    def get_queryset(self):
        queryset = Question.objects.filter_by_is_answered()
        queryset = self.apply_search_filter(queryset)

        return queryset

    def test_func(self):
        return self.request.user.groups.filter(name__exact='pharmacist').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        context['user'] = user
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

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
        patient = get_object_or_404(UserModel, pk=self.kwargs['user_pk'])
        try:
            answer = get_object_or_404(Answer, question_id_id=self.kwargs['question_pk'])
            pharmacist = get_object_or_404(UserModel, pk=answer.creator_id_id)
            comments = Comment.objects.filter(answer=answer)
            context['comments'] = comments
            context['answer'] = answer
            context['pharmacist'] = pharmacist
            context['like_form'] = LikeForm()
            context['dislike_form'] = DislikeForm()
            context['rating'] = Rating.objects.filter(answer_id=answer).first()

            paginator = Paginator(comments, 4)
            page = self.request.GET.get('page', 1)

            try:
                paginated_comments = paginator.page(page)
            except PageNotAnInteger:
                paginated_comments = paginator.page(1)
            except EmptyPage:
                paginated_comments = paginator.page(paginator.num_pages)

            context['paginated_comments'] = paginated_comments
        except Http404:
            pass

        context['patient'] = patient
        context['comment_form'] = CommentCreateForm()

        return context

    def post(self, request, *args, **kwargs):
        answer = get_object_or_404(Answer, question_id_id=self.kwargs['question_pk'])
        form = CommentCreateForm(request.POST)
        like_form = LikeForm(request.POST)
        dislike_form = DislikeForm(request.POST)
        form_type = request.POST.get('form_type')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = Question.objects.get_answer(kwargs['question_pk'])
            comment.author = self.request.user
            comment.save()
            return redirect(self.request.META.get('HTTP_REFERER'))

        if form_type == 'like_form':
            try:
                rating = Rating.objects.get(answer_id=answer, patient_id=request.user)
                if rating.like:
                    rating.like = False
                else:
                    rating.like = True
                    if rating.dislike:
                        rating.dislike = False
                rating.save()
            except Rating.DoesNotExist:
                rating = like_form.save(commit=False)
                rating.like = True
                rating.answer_id = answer
                rating.patient_id = request.user
                rating.save()

            return redirect(self.request.META.get('HTTP_REFERER'))

        if form_type == 'dislike_form':
            try:
                rating = Rating.objects.get(answer_id=answer, patient_id=request.user)
                if rating.dislike:
                    rating.dislike = False
                else:
                    rating.dislike = True
                    if rating.like:
                        rating.like = False
                rating.save()
            except Rating.DoesNotExist:
                rating = dislike_form.save(commit=False)
                rating.dislike = True
                rating.answer_id = answer
                rating.patient_id = request.user
                rating.save()

            return redirect(self.request.META.get('HTTP_REFERER'))
