from django.shortcuts import render, redirect
from django.views .generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Usuario, Concierto, Compra
from .forms import RegistroForm, LoginForm
from django.http.response import HttpResponse

#------------------------------------------------------------
# Listado de Todos los Conciertos Disponibles
# Nombre de plantilla: conciertosListado.html
#------------------------------------------------------------
def getListadoConciertos (request):
    conciertos = Concierto.objects.all()
    detalles_concierto = []

    for concierto in conciertos:
        detalles_concierto.append((
            concierto.id,
            concierto.artista,
            concierto.nombre_concierto,
            concierto.fecha_evento,
            concierto.num_tickets_disponibles,
            f'{concierto.id}_{concierto.artista}')
        )
    return render (request, 
                   'conciertosListado.html', 
                   {'listadoConcierto': detalles_concierto}
                )

#------------------------------------------------------------
# Reserva  de concierto:
#    Funcion de encargada de realizar la actualizacion del 
#    numero de tickets comprados y tickets disponibles
#------------------------------------------------------------
def reservaConcierto(request, infoCompra):
 #==> Datos del formulario
    tickets_comprados = int(request.POST['ticketsComprados'])

 #==> Datos de la Base:
    id_concierto = infoCompra['id']
    fecha_evento = infoCompra['fecha_evento']
    tickets_disponibles = infoCompra['num_tickets']
    precio_ticket = infoCompra['precio']

    if  tickets_disponibles >= tickets_comprados and fecha_evento > timezone.now() :
        total_factura = round(precio_ticket * tickets_comprados)
        ticket_comprado = Compra(total_compra = total_factura,
                                    cantidad_tickets = tickets_comprados,
                                    concierto_id = id_concierto,
                                    usuario_id = request.user.id
                                )
        ticket_comprado.save()

        concierto = Concierto.objects.get(id=id_concierto)
        concierto.num_tickets_disponibles -= tickets_comprados
        concierto.save()
        return True
    else:
        return False
    
#------------------------------------------------------------
# Listado de Informacion de un concierto en concreto
# Nombre de plantilla: infoConcierto.html
#------------------------------------------------------------
def getInfoConciertoById (request, id_concierto):
    concierto = Concierto.objects.get(id=id_concierto)
    contexto = {
        'id':id_concierto,
        'artista': concierto.artista,
        'nombre_concierto': concierto.nombre_concierto,
        'fecha_evento': concierto.fecha_evento,
        'num_tickets': concierto.num_tickets_disponibles,
        'descripcion_concierto': concierto.descripcion_artista,
        'precio': concierto.precio_ticket,
        'nombre_imagen': f'{id_concierto}_{concierto.artista}'
        }
    if request.method == 'POST':
        reserva = reservaConcierto(request, contexto)
        if reserva:
            messages.success(request, '¡Compra realizada con exito!')
            return redirect('mis-tickets')
        else:
            messages.error(request, '¡Lo Sentimos! Ha ocurrido un problema')

    return render (request, 'infoConcierto.html', contexto)


    
#------------------------------------------------------------
# Cancelacion de compra de tickets
# Funcion encargada de realizar hacer la cancelacion de un
# ticket comprado
#------------------------------------------------------------
def cancelarTicket (request):
  #==> Datos del formulario
  ticket_cancelado = int(request.POST['idTicket'][0])

  #==> Datos de la base
  info_ticketComprado = Compra.objects.get(id=ticket_cancelado)
  boletos_comprados = info_ticketComprado.cantidad_tickets

  info_conciertoComprado = Concierto.objects.get(id=info_ticketComprado.concierto_id)
  fecha_evento = info_conciertoComprado.fecha_evento

  fecha_actual = timezone.now()
  diferencia_dias = (fecha_actual - fecha_evento).days

  if diferencia_dias >= 2:
      info_ticketComprado.delete()
      info_conciertoComprado.num_tickets_disponibles += boletos_comprados
      info_conciertoComprado.save()
      



#------------------------------------------------------------
# Listado de Todos los Conciertos Reservados 
# Nombre de la plantilla: mis-tickets.html
#------------------------------------------------------------
def getConciertoReserva (request):
    id_user = request.user.id
    conciertos_comprados = Compra.objects.filter(usuario_id=id_user).order_by('concierto_id')
    detalles_portadas = {}
    detalles_comprados = {}
    for itemTicket in conciertos_comprados:
        concierto_id = str(itemTicket.concierto_id)
        if concierto_id not in detalles_comprados:
            detalle_concierto = Concierto.objects.get(id=itemTicket.concierto_id)
            detalles_portadas[concierto_id] = [detalle_concierto.nombre_concierto,
                                               detalle_concierto.artista,
                                               detalle_concierto.fecha_evento,
                                              f'{concierto_id}_{detalle_concierto.artista}']
            detalles_comprados[concierto_id] = [(itemTicket.id,
                                                itemTicket.fecha_compra,
                                                itemTicket.total_compra,
                                                itemTicket.cantidad_tickets,
                                                itemTicket.concierto_id,
                                                itemTicket.usuario_id)]
        else:
            detalles_comprados[concierto_id].append((
                itemTicket.id,
                itemTicket.fecha_compra,
                itemTicket.total_compra,
                itemTicket.cantidad_tickets,
                itemTicket.concierto_id,
                itemTicket.usuario_id
            ))
    if request.method == 'POST':
        cancelarTicket(request)
        return redirect(request.path)

    return render(request, 'mis-tickets.html', {'listadoPortada': detalles_portadas, 
                                                'listadoCompra':detalles_comprados                                                 
                                                })













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
                  template_name='login.html', 
                  context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrado sesión")
    return redirect("login")

    
class MainView (TemplateView):
    template_name = 'main.html'




