from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from empleados.utils.text import CharSet


# Un nombre solo permite letras y espacios
validar_nombre_simple = RegexValidator(
    regex=rf'^[{CharSet.LATIN_LETTERS}{CharSet.WHITESPACE}]+$',
    message="Este campo solo debe contener letras y espacios."
    
)

# El texto seguro permite letras, números, puntuación y saltos de línea
validar_texto_seguro = RegexValidator(
    regex=rf'^[{CharSet.LATIN_LETTERS}{CharSet.NUMBERS}{CharSet.WHITESPACE}{CharSet.PUNCTUATION}\n]+$',
    message="El texto contiene caracteres no permitidos (solo se permiten letras, números y puntuación básica)."
)

def validar_fecha_ingreso(fecha):

    if fecha > timezone.now().date():
        raise ValidationError(
            "La fecha de ingreso no puede ser mayor a la fecha actual."
        )