from django.db import models
from django.db import models
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.PROTECT, related_name='user', default=None)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15, null=True, blank=True)

class Concierto(models.Model):
    artista = models.CharField(max_length=100)
    nombre_concierto = models.CharField(max_length=100)
    fecha_evento = models.DateTimeField()
    num_tickets_disponibles = models.IntegerField()
    descripcion_artista = models.TextField()
    precio_ticket = models.FloatField()

class Compra(models.Model):
    fecha_compra = models.DateTimeField(default=timezone.now)
    total_compra = models.FloatField()
    cantidad_tickets = models.IntegerField(default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    concierto = models.ForeignKey(Concierto, on_delete=models.DO_NOTHING)

