from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from PharmaQ.accounts.forms import PatientEditForm
from PharmaQ.accounts.forms.common_forms import AppUserRegistrationForm

UserModel = get_user_model()

class PatientRegistrationView(CreateView):
    model = UserModel
    form_class = AppUserRegistrationForm
    template_name = 'accounts/patient-register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class PatientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserModel
    template_name = 'accounts/patient-details.html'
    context_object_name = 'user'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user


class PatientEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = PatientEditForm
    template_name = 'accounts/patient-edit.html'

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def get_success_url(self):
        patient_id = self.kwargs['pk']
        return reverse_lazy('patient-details', kwargs={'pk': patient_id})

