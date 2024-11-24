from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView

from PharmaQ.accounts.forms import PatientEditForm

UserModel = get_user_model()

class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'


class AppUserChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView):
    template_name = 'accounts/change-password.html'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy('user-details', kwargs={'pk':self.request.user.pk})


class AppUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/user-delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserModel
    template_name = 'accounts/user-details.html'
    context_object_name = 'user'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user


class PublicUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/user-details-public.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return user


