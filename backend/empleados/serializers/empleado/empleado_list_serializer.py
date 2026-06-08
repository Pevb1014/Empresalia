from rest_framework import serializers
from empleados.models import Empleado

class EmpleadoListSerializer(serializers.ModelSerializer):
    """
    Serializador optimizado para listados de Empleados.

    Aplana las relaciones de Cargo y Área para devolver únicamente los nombres
    como cadenas de texto, reduciendo el tamaño de la respuesta y facilitando
    su visualización en tablas o rejillas de datos.
    """
    area = serializers.CharField(source="cargo.area.nombre", read_only=True)
    cargo = serializers.CharField(source="cargo.nombre", read_only=True)

    class Meta:
        model = Empleado
        fields = [
            "id",
            "nombre",
            "area",
            "cargo"
        ]