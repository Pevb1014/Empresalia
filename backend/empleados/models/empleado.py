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
    """
    Representa un trabajador de la organización.

    Almacena la información maestra del personal y su posición actual a través del cargo.

    Atributos:
        id (UUIDField): Identificador único universal (UUID) del empleado.
        numero_documento (CharField): Documento de identidad único del empleado.
        nombre (CharField): Nombre completo del trabajador.
        correo (EmailField): Dirección de correo electrónico institucional única.
        cargo (ForeignKey): Cargo oficial asignado.
        fecha_ingreso (DateField): Fecha en la que inició su relación laboral.
        estado (CharField): Estado operativo actual (ACTIVO/INACTIVO).

    Comportamiento:
        - Normaliza nombres, correos y documentos antes de guardar.
        - Asegura que el correo sea único (Case-Insensitive).
        - Valida reglas de negocio (ej. fechas de ingreso válidas) mediante validadores.
    """

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