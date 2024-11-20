from django.urls import path
from PharmaQ.common.views import AppIndexView, send_test_email

urlpatterns = [
    path('', AppIndexView.as_view(), name='index'),
    path('email/', send_test_email, name='send-test-email'),
]