from django.core.exceptions import ValidationError
from django.utils import timezone


def validar_fecha_ingreso(fecha):

    if fecha > timezone.now().date():
        raise ValidationError(
            "La fecha de ingreso no puede ser mayor a la fecha actual."
        )
