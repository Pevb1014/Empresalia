# utils/text.py
import re

class CharSet:
    """Bloques de construcción para expresiones regulares."""
    LATIN_LETTERS = r'a-zA-ZáéíóúÁÉÍÓÚñÑ'
    NUMBERS = r'0-9'
    PUNCTUATION = r'.,;:\-()¿?¡!"\''
    WHITESPACE = r'\s'


def normalizar_texto(value: str | None) -> str | None:
    if not value:
        return value

    value = value.strip()

    value = re.sub(r"\s+", " ", value)

    return value


def normalizar_nombre(value: str | None) -> str | None:
    value = normalizar_texto(value)

    if not value:
        return value

    return value.title()


def normalizar_email(value: str | None) -> str | None:
    value = normalizar_texto(value)

    if not value:
        return value

    return value.lower()


def normalizar_documento(value: str | None) -> str | None:
    value = normalizar_texto(value)

    if not value:
        return value

    return (
        value
        .replace(".", "")
        .replace("-", "")
        .replace(" ", "")
    )