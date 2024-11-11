from django.contrib.auth.views import LogoutView
from django.urls import path, include
from PharmaQ.accounts.views import AppUserLoginView, PatientRegistrationView, PatientEditView, PatientDetailView, \
    AppUserDeleteView, AppUserChangePasswordView

urlpatterns = [
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register', include([
        path('patient/', PatientRegistrationView.as_view(), name='patient-registration'),
    ])),
    path('profile/<int:pk>/', include([
        path('details/', PatientDetailView.as_view(), name='patient-details'),
        path('edit/', PatientEditView.as_view(), name='patient-edit'),
        path('delete/', AppUserDeleteView.as_view(), name='patient-delete'),
        path('password-change/', AppUserChangePasswordView.as_view(), name='password-change'),
    ]))

]