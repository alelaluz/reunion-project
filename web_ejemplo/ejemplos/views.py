from django.contrib import messages
# from django.conf import setting
# from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from datetime import datetime
from ejemplos.forms import ContactoForm

# Create your views here.

# si yo no pongo nada en la url dispacher entonces entro en la pagina de inicio


def index(request):
    formulario_contacto = None
    if request.method == 'GET':
        formulario_contacto = ContactoForm()
    elif request.method == 'POST':
        formulario_contacto = ContactoForm(request.POST)
        # aca lo que hago es todo lo que impacta en el sistema (envio de mail, grabar datos etc )
        if formulario_contacto.is_valid():
            messages.success(request, 'hemos recibido los datosssss')
        else:
            messages.error(
                request, 'por favor revisa los errores en el formulario')
    else:
        return HttpResponseBadRequest("mandaste cualquiera ")
    contexto = {
        # 'ahora': datetime.now,
        'mi_formulario': formulario_contacto
    }

    return render(request, "ejemplos/index.html", contexto)


def cursos(request, ini):
    listado_cursos = [
        {
            'nombre': 'CURSO ESCALADA BASICA',
            'descripcion': 'principios de escalada ',
            'categoria': 'curso',
        },
        {
            'nombre': 'ASCENSO AL VOLCAN',
            'descripcion': 'ascensos a volcan Etna',
            'categoria': 'ascensos',
        },
        {
            'nombre': 'SALIDA DE TREKKING Y FOTOGRAFIA',
            'descripcion': 'salidas de trekking ',
            'categoria': 'trekking',
        },

    ]
    return render(request, "ejemplos/curso.html", {'cursos': listado_cursos})


def quienes_somos(request):
    return render(request, "ejemplos/quienes_somos.html")
