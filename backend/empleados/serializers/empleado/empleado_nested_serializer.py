from rest_framework import serializers

from empleados.models import Empleado


class EmpleadoNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empleado
        fields = (
            "id",
            "nombre",
        )