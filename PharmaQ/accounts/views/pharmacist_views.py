from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.db.models import Count, Q, F
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from PharmaQ.accounts.forms import AppUserRegistrationForm
from PharmaQ.accounts.forms.pharmacist_forms import PharmacistEditForm
from PharmaQ.common.mixins import SearchMixin

UserModel = get_user_model()

class PharmacistRegistrationView(CreateView):
    model = UserModel
    form_class = AppUserRegistrationForm
    template_name = 'accounts/pharmacist-register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        group = Group.objects.get(name='pharmacist')

        professional_card = self.request.FILES.get('professional-card')

        if professional_card is None:
            form.add_error(None, "Качването на файл е задължително.")
            return self.form_invalid(form)

        pharmacist = form.save(commit=False)
        pharmacist.is_patient = False
        pharmacist.is_pharmacist = True
        pharmacist.is_approved = False
        pharmacist.professional_card = professional_card
        response = super().form_valid(form)

        pharmacist.groups.add(group)

        return response

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['username'].label = 'Потребителско име'
        form.fields['email'].label = 'Имейл'
        form.fields['password1'].label = 'Парола'
        form.fields['password2'].label = 'Потвърди паролата'

        return form

class PharmacistEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = PharmacistEditForm
    template_name = 'accounts/user-edit.html'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def get_success_url(self):
        patient_id = self.kwargs['pk']
        return reverse_lazy('user-details', kwargs={'pk': patient_id})


class AllPharmacistListView(LoginRequiredMixin, SearchMixin, ListView):
    model = UserModel
    template_name = 'accounts/pharmacist-list-all.html'
    context_object_name = 'all_pharmacists'
    paginate_by = 5

    search_fields = ['username', 'first_name', 'last_name']

    def get_queryset(self, **kwargs):
        queryset = (UserModel.objects
                    .filter(groups__name='pharmacist', is_active=True, is_approved=True)
                    .annotate(likes=Count('answers__ratings', filter=Q(answers__ratings__like=True))
                              ,dislikes=Count('answers__ratings', filter=Q(answers__ratings__dislike=True)))
                    .annotate(rating=F('likes') - F('dislikes'))
                    .annotate(all_answers=Count('answers'))
                    .order_by('-rating', '-all_answers'))
        queryset = self.apply_search_filter(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class UnapprovedPharmacistListView(LoginRequiredMixin, UserPassesTestMixin, SearchMixin, ListView):
    model = UserModel
    template_name = 'accounts/pharmacist-approve.html'
    context_object_name = 'all_pharmacists'
    paginate_by = 5

    search_fields = ['username', 'first_name', 'last_name', 'email']

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])

        return user.groups.filter(name__exact='site-moderator').exists()

    def get_queryset(self, **kwargs):
        queryset = UserModel.objects.filter(groups__name='pharmacist', is_approved=False, is_active=True)
        queryset = self.apply_search_filter(queryset)
        return queryset


class AllPharmacistsModerationListView(LoginRequiredMixin, UserPassesTestMixin, SearchMixin, ListView):
    model = UserModel
    template_name = 'accounts/pharmacists-all-moderation.html'
    context_object_name = 'all_pharmacists'
    paginate_by = 5

    search_fields = ['username', 'first_name', 'last_name', 'email']

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return user.groups.filter(name__exact='site-moderator').exists()

    def get_queryset(self, **kwargs):
        queryset = (UserModel.objects.filter(groups__name='pharmacist', is_active=True)
                    .annotate(likes=Count('answers__ratings', filter=Q(answers__ratings__like=True))
                              ,dislikes=Count('answers__ratings', filter=Q(answers__ratings__dislike=True)))
                    .annotate(rating=F('likes') - F('dislikes'))
                    .annotate(all_answers=Count('answers'))
                    .order_by('-rating', '-all_answers'))
        queryset = self.apply_search_filter(queryset)
        return queryset


@login_required
def approve_pharmacist(request, pk):
    if request.method == 'POST':
        pharmacist = UserModel.objects.get(pk=pk)
        pharmacist.is_approved = True
        pharmacist.save()

    return redirect(request.META.get('HTTP_REFERER'))