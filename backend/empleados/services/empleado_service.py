from empleados.models import HistorialCambio, TipoCambio
from django.db import models

def auditar_actualizacion_empleado(empleado, valores_anteriores, valores_nuevos):
    """
    Compara los valores previos y nuevos de un empleado y registra las diferencias.

    Itera sobre un diccionario de nuevos valores y genera un registro en el
    HistorialCambio por cada atributo que haya sido modificado. Los valores
    de los campos ForeignKey se registran como su representación descriptiva
    (e.g., nombre) para mayor legibilidad.

    Args:
        empleado (Empleado): Instancia del empleado que está siendo actualizado.
        valores_anteriores (dict): Diccionario con los valores del objeto antes de guardar.
                                   Para ForeignKeys, contiene la instancia del objeto relacionado.
        valores_nuevos (dict): Diccionario con los datos validados recibidos para actualizar.
                               Para ForeignKeys, contiene la instancia del objeto relacionado.
    """
    historial_entries = []
    for campo, valor_nuevo_obj in valores_nuevos.items():
        valor_anterior_obj = valores_anteriores.get(campo)

        # Obtener el campo del modelo para determinar su tipo
        field = empleado._meta.get_field(campo)

        valor_anterior_str = None
        valor_nuevo_str = None

        if isinstance(field, models.ForeignKey):
            # Para ForeignKeys, `valor_anterior_obj` y `valor_nuevo_obj` ya son las instancias
            # del modelo relacionado (o None).
            valor_anterior_str = str(valor_anterior_obj) if valor_anterior_obj else None
            valor_nuevo_str = str(valor_nuevo_obj) if valor_nuevo_obj else None
        else:
            valor_anterior_str = str(valor_anterior_obj) if valor_anterior_obj is not None else None
            valor_nuevo_str = str(valor_nuevo_obj) if valor_nuevo_obj is not None else None

        if valor_anterior_str != valor_nuevo_str:
            historial_entries.append(
                HistorialCambio(
                    empleado=empleado,
                    tipo_cambio=TipoCambio.ACTUALIZACION,
                    campo_cambiado=campo,
                    valor_anterior=valor_anterior_str,
                    valor_nuevo=valor_nuevo_str
                )
            )
    if historial_entries:
        HistorialCambio.objects.bulk_create(historial_entries)

def auditar_creacion_empleado(empleado):
    """
    Registra el estado inicial de todos los campos de un nuevo empleado.

    Utiliza la introspección de Django (_meta) para recorrer todos los campos
    definidos en el modelo y crear un rastro de auditoría tipo 'CREACION'.
    Los valores de los campos ForeignKey se registran como su representación
    descriptiva (e.g., nombre) para mayor legibilidad.

    Args:
        empleado (Empleado): La instancia del empleado recién creada.
    """
    historial_entries = []
    for field in empleado._meta.fields:
        if field.name == "id":
            continue

        valor_nuevo = getattr(empleado, field.name)

        # Manejo especial para ForeignKey
        if isinstance(field, models.ForeignKey):
            # Si el campo ForeignKey tiene un valor (no es None)
            if valor_nuevo:
                # Acceder al atributo descriptivo del objeto relacionado
                # Asumimos que todos los modelos relacionados tienen un atributo 'nombre'
                # o una representación __str__ significativa.
                related_object = getattr(empleado, field.name)
                valor_nuevo_str = str(related_object)
            else:
                valor_nuevo_str = None  # Si el ForeignKey es nulo
        else:
            valor_nuevo_str = str(valor_nuevo) if valor_nuevo is not None else None

        historial_entries.append(
            HistorialCambio(
                empleado=empleado,
                tipo_cambio=TipoCambio.CREACION,
                campo_cambiado=field.name,
                valor_anterior=None,
                valor_nuevo=valor_nuevo_str
            )
        )
    if historial_entries:
        HistorialCambio.objects.bulk_create(historial_entries)