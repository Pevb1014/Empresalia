from django.contrib import admin
from .models import Area, Cargo, Empleado, HistorialCambio

admin.site.register(Area)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(HistorialCambio)