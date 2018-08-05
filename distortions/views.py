from django.db import IntegrityError
from django.http import HttpResponse
from django.template import loader

from .models import TrapType


def index(request):
    if request.method == 'POST':
        try:
            trap_name = request.POST.get('trap_name')
            trap_type = TrapType(name=trap_name, description=None)
            trap_type.save()
        except IntegrityError:
            pass
    template = loader.get_template("index.html")
    context = {'traps': TrapType.objects.all()}
    return HttpResponse(template.render(context, request))
