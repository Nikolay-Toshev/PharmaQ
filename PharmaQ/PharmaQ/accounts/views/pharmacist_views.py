from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from PharmaQ.accounts.forms import AppUserRegistrationForm
from PharmaQ.accounts.forms.pharmacist_forms import PharmacistEditForm

UserModel = get_user_model()

class PharmacistRegistrationView(CreateView):
    model = UserModel
    form_class = AppUserRegistrationForm
    template_name = 'accounts/user-register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        pharmacist = form.save(commit=False)
        pharmacist.is_patient = False
        pharmacist.is_pharmacist = True
        response = super().form_valid(form)
    
        login(self.request, self.object)

        return response

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
