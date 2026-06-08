import uuid

from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from empleados.models.area import Area
from empleados.utils.text import normalizar_nombre, normalizar_texto
from empleados.validators.validators import validar_texto_seguro, validar_nombre


class Cargo(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Identificador único universal (UUID) del cargo."
    )

    nombre = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            validar_nombre
        ],
        help_text="Nombre único identificativo del cargo corporativo"
    )

    descripcion = models.TextField(
        blank=True, 
        null=True,
        validators=[
            MaxLengthValidator(1000),
            validar_texto_seguro
        ],
        help_text="Breve descripción de las funciones y responsabilidades del cargo (máximo 1000 caracteres)."
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="cargos",
        help_text="Área corporativa a la que pertenece este cargo."
    )

    class Meta:
        db_table = "cargos"
        ordering = ["nombre"]

        constraints = [
            UniqueConstraint(
                Lower("nombre"),
                name="unique_cargo_nombre_ci",
                violation_error_message="Ya existe un cargo registrado con este nombre."
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.area.nombre})"

    def save(self, *args, **kwargs):
        self.nombre = normalizar_nombre(self.nombre)
        self.descripcion = normalizar_texto(self.descripcion)
        self.full_clean()
        super().save(*args, **kwargs)