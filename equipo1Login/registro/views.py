from django.shortcuts import render
from requests import request
from django.http import JsonResponse
from core.models import Contacto
from .forms import ContactoForm


def registro(request):
    form = ContactoForm()
    return render(request, "registro/registro.html", {
        "form": form
    })


def contacto_view(request):
    todos = Contacto.objects.all()  # consulta a la base de datos para traer todos los contactos
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
             form = ContactoForm(request.POST)
        if form.is_valid():
            # Los datos ya pasaron las validaciones de front y back
            form.save()  # Guarda el contacto en la base de datos

            return JsonResponse({'status':'ok', 'message':'Contacto registrado exitosamente'})
        else:
            return JsonResponse({'status':'error', 'message':'Datos inválidos', 'errors': form.errors}, status = 400)
    else:
        form = ContactoForm()

        
    return render(request, "registro/registro.html", {
        "form": form    })
