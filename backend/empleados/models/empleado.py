import uuid

from django.db import models
from .area import Area
from .cargo import Cargo
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from empleados.validators import validar_fecha_ingreso
from empleados.utils.text import normalize_email, normalize_name

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
        max_length=50,
        help_text="Número de documento de identidad único del empleado."
    )

    nombre = models.CharField(
        max_length=150,
        help_text="Nombre completo del empleado."
    )

    correo = models.EmailField(
        help_text="Dirección de correo electrónico institucional o de contacto del empleado."
    )

    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name="empleados",
        help_text="Cargo oficial asignado que define sus funciones laborales."
    )

    fecha_ingreso = models.DateField(
        validators=[validar_fecha_ingreso],
        help_text="Fecha oficial en la que el empleado ingresó a trabajar en la empresa (Formato: AAAA-MM-DD)."
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

    def clean(self):
        if self.cargo and self.area:
            if self.cargo.area_id != self.area_id:
                raise ValidationError("El cargo no pertenece al área seleccionada.")

    def save(self, *args, **kwargs):
        self.clean()

        self.nombre = normalize_name(self.nombre)
        self.correo = normalize_email(self.correo)
        self.numero_documento = self.numero_documento.strip()

        super().save(*args, **kwargs)