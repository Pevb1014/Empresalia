from rest_framework import serializers

from empleados.models import Empleado


class EmpleadoNestedSerializer(serializers.ModelSerializer):
    """
    Representación minimalista de un Empleado.

    Diseñado para ser anidado dentro de otros serializadores donde solo se 
    requiere la identidad básica (ID y Nombre) del trabajador.
    """

    class Meta:
        model = Empleado
        fields = (
            "id",
            "nombre",
        )