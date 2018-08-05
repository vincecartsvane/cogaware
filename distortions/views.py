from django.http import HttpResponse
from django.template import loader

from .models import TrapType


def index(request):
    if request.method == 'POST':
        trap_name = request.POST.get('trap_name')
        trap_type = TrapType(name=trap_name, description=None)
        trap_type.save()
    template = loader.get_template("index.html")
    context = {'traps': TrapType.objects.all()}
    return HttpResponse(template.render(context, request))
