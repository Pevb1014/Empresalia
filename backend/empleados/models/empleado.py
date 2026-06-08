import uuid

from django.db import models
from .cargo import Cargo
from django.db.models import UniqueConstraint
from django.core.validators import MinLengthValidator
from django.db.models.functions import Lower
from empleados.validators.validators import (
    validar_nombre, 
    validar_fecha_ingreso,
    validar_numero_documento,
    validar_email_corporativo
)
from empleados.utils.text import normalizar_documento, normalizar_email, normalizar_nombre
from empleados.utils.dates import normalizar_fecha_a_date

class EstadoEmpleado(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"

class Empleado(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Identificador único universal (UUID) del empleado."
    )

    numero_documento = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(5),
            validar_numero_documento
        ],
        help_text="Número de documento de identidad único del empleado."
    )

    nombre = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            validar_nombre
        ],
        help_text="Nombre del empleado (máximo 100 caracteres)."
    )

    correo = models.EmailField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            validar_email_corporativo
        ],
        help_text="Dirección de correo electrónico institucional del empleado."
    )

    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name="empleados",
        help_text="Cargo oficial asignado que define sus funciones laborales."
    )

    fecha_ingreso = models.DateField(
        validators=[validar_fecha_ingreso],
        help_text="Fecha en la que el empleado ingresó a trabajar en la empresa."
    )

    estado = models.CharField(
        max_length=10,
        choices=EstadoEmpleado.choices,
        default=EstadoEmpleado.ACTIVO,
        help_text="Estado operativo del empleado en el sistema (ACTIVO/INACTIVO)."
    )

    class Meta:
        db_table = "empleados"
        ordering = ["nombre"]

        constraints = [
            UniqueConstraint(Lower("correo"), name="unique_correo_ci"),
            UniqueConstraint("numero_documento", name="unique_documento")
        ]

    def __str__(self):
        return f"{self.nombre} - {self.numero_documento}"


    def save(self, *args, **kwargs):
        self.nombre = normalizar_nombre(self.nombre)
        self.correo = normalizar_email(self.correo)
        self.numero_documento = normalizar_documento(self.numero_documento)
        self.fecha_ingreso = normalizar_fecha_a_date(self.fecha_ingreso)

        self.full_clean()
        super().save(*args, **kwargs)