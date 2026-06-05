from rest_framework import serializers
from empleados.models import Empleado

class EmpleadoListSerializer(serializers.ModelSerializer):
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