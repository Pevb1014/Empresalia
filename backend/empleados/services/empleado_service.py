from empleados.models import HistorialCambio, TipoCambio

def registrar_cambios_empleado(empleado, valores_anteriores, valores_nuevos):
    for campo, valor_nuevo in valores_nuevos.items():
        valor_anterior = valores_anteriores.get(campo)
        
        if valor_anterior != valor_nuevo:
            HistorialCambio.objects.create(
                empleado=empleado,
                tipo_cambio=TipoCambio.ACTUALIZACION,
                campo_cambiado=campo,
                valor_anterior=str(valor_anterior) if valor_anterior is not None else None,
                valor_nuevo=str(valor_nuevo) if valor_nuevo is not None else None
            )

def registrar_creacion_empleado(empleado):
    for field in empleado._meta.fields:
        if field.name == "id":
            continue

        HistorialCambio.objects.create(
            empleado=empleado,
            tipo_cambio=TipoCambio.CREACION,
            campo_cambiado=field.name,
            valor_anterior=None,
            valor_nuevo=str(getattr(empleado, field.name))
        )