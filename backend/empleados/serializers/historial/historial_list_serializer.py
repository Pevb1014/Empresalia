from rest_framework import serializers
from empleados.models import HistorialCambio


class HistorialListSerializer(serializers.ModelSerializer):

    empleado = serializers.CharField(source="empleado.nombre", read_only=True)

    class Meta:
        model = HistorialCambio
        fields = [
            "id",
            "empleado",
            "fecha_cambio",
            "tipo_cambio"
        ]