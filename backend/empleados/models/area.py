import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.core.validators import MaxLengthValidator, MinLengthValidator
from empleados.validators.validators import validar_texto_seguro, validar_nombre
from empleados.utils.text import normalizar_nombre, normalizar_texto


class Area(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único universal (UUID) del área corporativa."
    )

    nombre = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            validar_nombre
        ],
        help_text="Nombre único identificativo del área corporativa"
    )

    descripcion = models.TextField(
        blank=True, 
        null=True,
        validators=[
            MaxLengthValidator(1000),
            validar_texto_seguro
        ],
        help_text="Breve descripción de las funciones y responsabilidades del área (máximo 1000 caracteres)."
    )

    class Meta:
        db_table = "areas"
        ordering = ["nombre"]
        constraints = [
            UniqueConstraint(
                Lower("nombre"),
                name="unique_area_nombre_ci",
                violation_error_message="Ya existe un área registrada con este nombre."
            ),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = normalizar_nombre(self.nombre)
        self.descripcion = normalizar_texto(self.descripcion)
        self.full_clean()
        super().save(*args, **kwargs)