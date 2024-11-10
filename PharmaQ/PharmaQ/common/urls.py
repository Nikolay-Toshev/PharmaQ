from django.urls import path
from PharmaQ.common.views import AppIndexView

urlpatterns = [
    path('', AppIndexView.as_view(), name='index'),
]