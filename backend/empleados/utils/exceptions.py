from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado para estandarizar las respuestas de error.
    Transforma los errores de DRF en un formato:
    {
        "status": "error",
        "errors": [
            {"campo": "nombre_del_campo", "mensaje": "descripción del error"}
        ]
    }
    """
    # Obtener la respuesta estándar de DRF primero
    response = exception_handler(exc, context)

    if response is not None:
        custom_errors = []

        if isinstance(exc, ValidationError):
            # exc.detail puede ser un dict (errores de campo) o una lista (errores generales)
            if isinstance(response.data, dict):
                for campo, mensajes in response.data.items():
                    # Aseguramos que el mensaje sea un string (DRF a veces envía listas)
                    mensaje = mensajes[0] if isinstance(mensajes, list) else mensajes
                    custom_errors.append({
                        "campo": campo,
                        "mensaje": mensaje
                    })
            elif isinstance(response.data, list):
                for msg in response.data:
                    custom_errors.append({
                        "campo": "detalle",
                        "mensaje": msg
                    })

            response.data = {
                "status": "error",
                "errors": custom_errors
            }

    return response
