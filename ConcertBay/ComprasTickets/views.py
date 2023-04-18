from django.shortcuts import render
from django.views .generic import TemplateView
from .models import Concierto

# Create your views here.


def getListadoConciertos (request):
    conciertos = Concierto.objects.all()
    detalles_concierto = []

    for concierto in conciertos:
        detalles_concierto.append((
            concierto.id,
            concierto.artista,
            concierto.nombre_concierto,
            concierto.fecha_evento,
            concierto.num_tickets_disponibles)
        )
    
    return render (request, 'conciertos.html', {'listadoConcierto': detalles_concierto})


def getInfoConciertoById (request, id_concierto):
    concierto = Concierto.objects.get(id=id_concierto)
    contexto = {
        'artista': concierto.artista,
        'nombre_concierto': concierto.nombre_concierto,
        'fecha_evento': concierto.fecha_evento,
        'num_tickets': concierto.num_tickets_disponibles,
        'descripcion': concierto.descripcion_artista,
        'precio': concierto.precio_ticket
    }
    return render (request, 'reservaConcierto.html', contexto)


class MainView (TemplateView):
    template_name = 'main.html'




