from django.views.generic.base import TemplateView


# Create your views here.
class AboutAuthorView(TemplateView):
    template_name = 'posts/about_author.html'


class AboutTechView(TemplateView):
    template_name = 'posts/about_tech.html'
