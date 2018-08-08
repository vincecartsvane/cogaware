from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
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
        return HttpResponseRedirect(reverse("index"))
    template = loader.get_template("index.html")
    context = {'traps': TrapType.objects.all()}
    return HttpResponse(template.render(context, request))


def trap(request, trap_id):
    trap = get_object_or_404(TrapType, id=trap_id)
    if request.method == 'DELETE':
        trap.delete()
        return HttpResponseRedirect(reverse("index"))
    if request.method == 'POST':
        trap.description = request.POST.get('description')
        trap.save()
        return HttpResponseRedirect(reverse('trap', args=[trap.id]))
    return render(request, "trap.html", {'trap': trap})
