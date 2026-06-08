from rest_framework import serializers
from empleados.models import HistorialCambio


class HistorialDetailSerializer(serializers.ModelSerializer):
    """
    Serializador detallado para un evento de auditoría.

    Expone todos los campos del modelo HistorialCambio, incluyendo los valores
    técnicos 'anterior' y 'nuevo' para un análisis profundo del cambio.
    """

    empleado = serializers.CharField(source="empleado.nombre", read_only=True)
    cargo = serializers.CharField(source="empleado.cargo.nombre", read_only=True)
    area = serializers.CharField(source="empleado.cargo.area.nombre", read_only=True)

    class Meta:
        model = HistorialCambio
        fields = "__all__"