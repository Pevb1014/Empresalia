import uuid

from django.db import models
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
from django.core.validators import MaxLengthValidator
from empleados.utils.text import normalize_name, normalize_text


class Area(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único universal (UUID) del área corporativa."
    )

    nombre = models.CharField(
        max_length=100,
        help_text="Nombre único identificativo del área corporativa (ej. Tecnología, Recursos Humanos)."
    )

    descripcion = models.TextField(
        validators=[MaxLengthValidator(500)],
        blank=True, 
        null=True,
        help_text="Breve descripción de las funciones y responsabilidades del área (máximo 500 caracteres)."
    )

    class Meta:
        db_table = "areas"
        ordering = ["nombre"]

        constraints = [
            UniqueConstraint(
                Lower("nombre"),
                name="unique_area_nombre_ci"
            )
        ]

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        self.nombre = normalize_name(self.nombre)
        self.descripcion = normalize_text(self.descripcion)
        super().save(*args, **kwargs)