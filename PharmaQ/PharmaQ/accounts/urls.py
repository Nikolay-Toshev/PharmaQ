from django.contrib.auth.views import LogoutView
from django.urls import path, include
from PharmaQ.accounts.views import AppUserLoginView, PatientRegistrationView, PatientEditView, UserDetailView, \
    AppUserDeleteView, AppUserChangePasswordView, PharmacistRegistrationView, PharmacistEditView

urlpatterns = [
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register', include([
        path('patient/', PatientRegistrationView.as_view(), name='patient-registration'),
        path('pharmacist/', PharmacistRegistrationView.as_view(), name='pharmacist-registration'),
    ])),
    path('profile/<int:pk>/', include([
        path('details/', UserDetailView.as_view(), name='user-details'),
        path('edit/patient/', PatientEditView.as_view(), name='patient-edit'),
        path('edit/pharmacist/', PharmacistEditView.as_view(), name='pharmacist-edit'),
        path('delete/', AppUserDeleteView.as_view(), name='user-delete'),
        path('password-change/', AppUserChangePasswordView.as_view(), name='password-change'),
    ]))

]