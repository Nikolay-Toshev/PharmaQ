from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path, include

from PharmaQ.accounts.views import AppUserLoginView, PatientRegistrationView, PatientEditView, AppUserDetailView, \
    AppUserDeleteView, AppUserChangePasswordView, PharmacistRegistrationView, PharmacistEditView, AllPharmacistListView, \
    PublicAppUserDetailView, UnapprovedPharmacistListView, approve_pharmacist, AllPharmacistsModerationListView, \
    AllPatientsModerationListView, AppUserPasswordResetView, AppUserPasswordResetConfirmView

urlpatterns = [
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset_password/', AppUserPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', PasswordResetDoneView.as_view(template_name='accounts/reset-password-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', AppUserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password-reset-complete.html'), name='password_reset_complete'),
    path('<int:pk>/', include([
        path('approve/', UnapprovedPharmacistListView.as_view(), name='approve'),
        path('pharmacists/', AllPharmacistsModerationListView.as_view(), name='pharmacists-moderation'),
        path('patients/', AllPatientsModerationListView.as_view(), name='patients-moderation'),
    ])),
    path('register', include([
        path('patient/', PatientRegistrationView.as_view(), name='patient-registration'),
        path('pharmacist/', PharmacistRegistrationView.as_view(), name='pharmacist-registration'),
    ])),
    path('pharmasists/', AllPharmacistListView.as_view(), name='pharmacist-list-all'),
    path('profile/<int:pk>/', include([
        path('approve/', approve_pharmacist, name="pharmacist-approve"),
        path('details/', AppUserDetailView.as_view(), name='user-details'),
        path('public-details/', PublicAppUserDetailView.as_view(), name='user-public-details'),
        path('edit/patient/', PatientEditView.as_view(), name='patient-edit'),
        path('edit/pharmacist/', PharmacistEditView.as_view(), name='pharmacist-edit'),
        path('delete/', AppUserDeleteView.as_view(), name='user-delete'),
        path('password-change/', AppUserChangePasswordView.as_view(), name='password-change'),
    ]))

]

