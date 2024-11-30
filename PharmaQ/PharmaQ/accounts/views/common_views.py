from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView

from PharmaQ.rating.models import Rating

UserModel = get_user_model()

class AppUserLoginView(LoginView, UserPassesTestMixin):
    template_name = 'accounts/login.html'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.request.user.id)
        return user.is_active

    def handle_no_permission(self):
        return redirect('index')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        if user.is_pharmacist:
            likes = Rating.objects.filter(answer_id__creator_id=user, like__exact=True).count()
            dislikes = Rating.objects.filter(answer_id__creator_id=user, dislike__exact=True).count()
            rating =  likes - dislikes
            context['rating'] = rating
        return context



class PublicUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/user-details-public.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return user


