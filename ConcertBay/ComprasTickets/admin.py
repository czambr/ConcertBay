from django.contrib import admin

from .models import Usuario, Concierto, Compra

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Concierto)
admin.site.register(Compra)

