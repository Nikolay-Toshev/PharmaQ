from django.contrib.auth import get_user_model, login
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


class PatientDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/patient-details.html'
    context_object_name = 'user'


class PatientEditView(UpdateView):
    model = UserModel
    form_class = PatientEditForm
    template_name = 'accounts/patient-edit.html'

    def get_success_url(self):
        patient_id = self.kwargs['pk']
        return reverse_lazy('patient-details', kwargs={'pk': patient_id})


class PatientDeleteView(DeleteView):
    model = UserModel
    template_name = 'accounts/patient-delete.html'
    success_url = reverse_lazy('index')


