from django.contrib.auth.views import LoginView, LogoutView


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'
