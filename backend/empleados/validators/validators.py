import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from empleados.utils.text import CharSet

def validar_nombre(texto):
    """
    Valida que el nombre contenga exclusivamente letras y espacios.

    Utiliza el conjunto de caracteres latinos definido en CharSet para soportar
    tildes y la letra 'ñ'.

    Args:
        texto (str): El nombre a validar.

    Raises:
        ValidationError: Si el texto está vacío o contiene números/símbolos.
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
    Verifica que el texto no contenga caracteres especiales no permitidos.

    Permite letras, números, puntuación básica (.,;:-()¿?¡!"') y saltos de línea.
    Es ideal para campos de descripción o notas.

    Args:
        texto (str | None): El texto a validar.

    Returns:
        str | None: El mismo texto si es válido.

    Raises:
        ValidationError: Si contiene caracteres fuera del conjunto permitido.
    """
    if not texto:
        return texto

    regex = rf'^[{CharSet.LATIN_LETTERS}{CharSet.NUMBERS}{CharSet.WHITESPACE}{CharSet.PUNCTUATION}\n]+$'
    if not re.match(regex, texto):
        raise ValidationError(
            "El texto contiene caracteres no permitidos (solo se permiten letras, números y puntuación básica)."
        )


def validar_fecha_ingreso(fecha):
    """
    Valida que la fecha de ingreso sea lógica y coherente.

    Reglas:
    1. La fecha no puede ser nula.
    2. Debe ser un objeto de tipo date.
    3. No puede ser una fecha futura respecto al día de hoy.

    Args:
        fecha (date): La fecha de ingreso proporcionada.

    Raises:
        ValidationError: Si la fecha es inválida o futura.
    """
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
    Valida que el número de documento consista únicamente en dígitos.

    No permite puntos, guiones ni espacios. Se espera que la normalización
    ocurra antes de esta validación.

    Args:
        texto (str): El número de documento.

    Raises:
        ValidationError: Si el texto contiene caracteres no numéricos.
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
    Asegura que el correo electrónico pertenezca al dominio oficial.

    Args:
        email (str): La dirección de correo.

    Raises:
        ValidationError: Si el correo no termina en @empresalia.com.
    """
    if not email:
        raise ValidationError("El correo electrónico es obligatorio.")

    dominio_corporativo = "empresalia.com"
    if not email.lower().endswith(f"@{dominio_corporativo}"):
        raise ValidationError(
            f"El correo debe pertenecer al dominio corporativo @{dominio_corporativo}."
        )
