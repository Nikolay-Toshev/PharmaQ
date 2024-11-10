from django.shortcuts import render
from django.views.generic import TemplateView


class AppIndexView(TemplateView):
    template_name = 'common/index.html'
