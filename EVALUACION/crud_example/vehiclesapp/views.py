from django.shortcuts import render, HttpResponseRedirect,get_object_or_404

# Create your views here.

from .models import vehiculo
from .forms import vehiculoForm

def create_view(request):
    context = {}
    form = vehiculoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")
    
    context['form'] = form
    return render(request, "create_view.html", context)

def list_view(request):
    context = {}
    context['dataset'] = vehiculo.objects.all()
    return render(request, "list_view.html", context)