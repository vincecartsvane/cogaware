from django.http import HttpResponse
from django.template import loader

from .models import TrapType


def index(request):
    template = loader.get_template("index.html")
    context = {'traps': TrapType.objects.all()}
    return HttpResponse(template.render(context, request))
