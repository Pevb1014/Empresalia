import uuid

from django.db import models

from .empleado import Empleado

class TipoCambio(models.TextChoices):
    CREACION = "CREACION", "Creación"
    ACTUALIZACION = "ACTUALIZACION", "Actualización"


class HistorialCambio(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Identificador único universal (UUID) de la auditoría de cambio."
    )

    fecha_cambio = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="Fecha y hora exacta en la que se efectuó y registró el cambio de manera automática."
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        editable=False,
        related_name="historial",
        help_text="Empleado que sufrió la modificación en sus datos."
    )

    tipo_cambio = models.CharField(
        max_length=20,
        choices=TipoCambio.choices,
        editable=False,
        help_text="Tipo de operación ejecutada sobre el registro del empleado (CREACION, ACTUALIZACION)."
    )

    campo_cambiado = models.CharField(
        max_length=100,
        editable=False,
        help_text="Nombre del atributo o columna específica que fue modificada."
    )

    valor_anterior = models.TextField(
        null=True, 
        blank=True,
        editable=False,
        help_text="Valor que tenía el campo antes del cambio (permanece vacío si el tipo es CREACION)."
    )

    valor_nuevo = models.TextField(
        null=True, 
        blank=True,
        editable=False,
        help_text="Nuevo valor asignado al campo tras la modificación realizada."
    )

    class Meta:
        db_table = "historial_cambios"
        ordering = ["-fecha_cambio"]

    def __str__(self):
        return f"{self.empleado_id} - {self.tipo_cambio} - {self.fecha_cambio}"