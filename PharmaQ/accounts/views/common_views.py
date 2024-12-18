from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView

from PharmaQ.accounts.utils import get_pharmacist_rating

UserModel = get_user_model()

class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_approved:
            return redirect('not-approved')

        login(self.request, user)
        return redirect('index')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['username'].label = 'Потребителско име'
        form.fields['password'].label = 'Парола'

        return form


class AppUserChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView):
    template_name = 'accounts/change-password.html'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy('user-details', kwargs={'pk':self.request.user.pk})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.fields['old_password'].label = 'Текуща парола'
        form.fields['new_password1'].label = 'Нова парола'
        form.fields['new_password2'].label = 'Потвърдете новата парола'

        return form


class AppUserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password-reset.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['email'].label = 'Имейл'

        return form


class AppUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['new_password1'].label = 'Нова парола'
        form.fields['new_password2'].label = 'Потвърдете новата парола'
        return form

class AppUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/user-delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        user.is_active = False
        user.save()

        if self.request.user == user:
            from django.contrib.auth import logout
            logout(request)

        return redirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class AppUserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserModel
    template_name = 'accounts/user-details.html'
    context_object_name = 'user'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        if user.is_pharmacist:
            context['rating'] = get_pharmacist_rating(user)
            context['answers'] = user.answers.count()
        return context



class PublicAppUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/user-details-public.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        if user.is_pharmacist:
            context['rating'] = get_pharmacist_rating(user)
            context['answers'] = user.answers.count()
        return context


