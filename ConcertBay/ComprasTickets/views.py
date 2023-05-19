from django.shortcuts import render, redirect
from django.views .generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import datetime
from .models import Usuario, Concierto
from .forms import RegistroForm, LoginForm


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


def registro_request(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user_CI = form.cleaned_data['cedula']
            if Usuario.objects.filter(cedula=user_CI).exists():
                messages.error(request, 'Este usuario ya existe')
            else:
                user = form.save()
                login(request, user)
                messages.success(request, 'Se ha registrado exitosamente')
                return redirect("landing")
        else:
            messages.error(request, 'Campos erroneos')
    # Si el formulario no fue válido, retorna formulario vacío
    form = RegistroForm()
    return render(request=request,
                  template_name='registro.html', 
                  context={'registro_form': form})


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Ha iniciado sesión como: {username}')
                return redirect("landing")
            messages.error(request, 'Credenciales incorrectas')
        messages.error(request, 'Credenciales incorrectas')
    # Método no válido, retorna formulario vacío
    form = LoginForm()
    return render(request=request, 
                  template_name='login-2.html', 
                  context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrado sesión")
    return redirect("login")

    
class MainView (TemplateView):
    template_name = 'main.html'




