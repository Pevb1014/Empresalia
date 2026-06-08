from rest_framework import serializers
from empleados.models import HistorialCambio


class HistorialListSerializer(serializers.ModelSerializer):

    empleado = serializers.CharField(source="empleado.nombre", read_only=True)
    cargo = serializers.CharField(source="empleado.cargo.nombre", read_only=True)
    area = serializers.CharField(source="empleado.cargo.area.nombre", read_only=True)

    class Meta:
        model = HistorialCambio
        fields = [
            "id",
            "empleado",
            "cargo",
            "area",
            "fecha_cambio",
            "tipo_cambio"
        ]