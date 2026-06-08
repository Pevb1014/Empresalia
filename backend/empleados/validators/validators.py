import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from empleados.utils.text import CharSet


def validar_nombre(texto):
    """
    Valida que el nombre contenga solo letras y espacios.
    Se usa función en lugar de RegexValidator para mayor control.
    """
    if not texto:
        raise ValidationError("El nombre no puede estar vacío.")

    regex = rf'^[{CharSet.LATIN_LETTERS}{CharSet.WHITESPACE}]+$'
    if not re.match(regex, texto):
        raise ValidationError(
            "Este campo solo debe contener letras y espacios."
        )


def validar_texto_seguro(texto):
    """
    Valida que el texto solo contenga caracteres seguros: letras, números, espacios y puntuación básica.
    Se usa función en lugar de RegexValidator para mayor control.
    """
    if not texto:
        return texto

    regex = rf'^[{CharSet.LATIN_LETTERS}{CharSet.NUMBERS}{CharSet.WHITESPACE}{CharSet.PUNCTUATION}\n]+$'
    if not re.match(regex, texto):
        raise ValidationError(
            "El texto contiene caracteres no permitidos (solo se permiten letras, números y puntuación básica)."
        )


def validar_fecha_ingreso(fecha):
    if fecha is None:
        raise ValidationError("La fecha de ingreso es obligatoria.")

    if not isinstance(fecha, date):
        raise ValidationError("El valor proporcionado debe ser una fecha válida.")

    if fecha > timezone.now().date():
        raise ValidationError(
            "La fecha de ingreso no puede ser mayor a la fecha actual."
        )


def validar_numero_documento(texto):
    """
    Valida que el número de documento contenga solo números, sin espacios.
    """
    if not texto:
        raise ValidationError("El número de documento es obligatorio.")

    regex = rf'^[{CharSet.NUMBERS}]+$'
    if not re.match(regex, texto):
        raise ValidationError(
            "El número de documento solo puede contener números, sin espacios ni símbolos."
        )


def validar_email_corporativo(email):
    """
    Valida que el correo electrónico pertenezca al dominio de la empresa.
    """
    if not email:
        raise ValidationError("El correo electrónico es obligatorio.")

    dominio_corporativo = "empresalia.com"
    if not email.lower().endswith(f"@{dominio_corporativo}"):
        raise ValidationError(
            f"El correo debe pertenecer al dominio corporativo @{dominio_corporativo}."
        )
