from django.urls import path
from PharmaQ.common.views import AppIndexView, AppHowToView

urlpatterns = [
    path('', AppIndexView.as_view(), name='index'),
    path('how-to-use/', AppHowToView.as_view(), name='how-to-use'),
]