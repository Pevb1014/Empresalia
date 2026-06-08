import uuid

from django.db import models
from django.core.validators import MaxLengthValidator
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from empleados.models.area import Area
from empleados.utils.text import normalizar_nombre, normalizar_texto
from empleados.validators import validar_nombre_simple


class Cargo(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Identificador único universal (UUID) del cargo."
    )

    nombre = models.CharField(
        max_length=100,
        validators=[validar_nombre_simple],
        help_text="Nombre asignado al cargo u ocupación dentro de la empresa."
    )

    descripcion = models.TextField(
        validators=[MaxLengthValidator(500)],
        blank=True,
        null=True,
        help_text="Descripción detallada de las tareas asignadas al cargo (máximo 500 caracteres)."
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="cargos",
        help_text="Área organizativa a la que pertenece estructuralmente este cargo."
    )

    class Meta:
        db_table = "cargos"
        ordering = ["nombre"]

        constraints = [
            UniqueConstraint(
                Lower("nombre"),
                name="unique_cargo_nombre_ci"
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.area.nombre})"

    def save(self, *args, **kwargs):
        self.nombre = normalizar_nombre(self.nombre)
        self.descripcion = normalizar_texto(self.descripcion)
        super().save(*args, **kwargs)