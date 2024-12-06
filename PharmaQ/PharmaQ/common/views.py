from django.views.generic import TemplateView


class AppIndexView(TemplateView):
    template_name = 'common/index.html'


class AppHowToView(TemplateView):
    template_name = 'common/hou-to-use.html'



