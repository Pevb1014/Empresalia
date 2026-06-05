from rest_framework import serializers
from empleados.models import Empleado
from empleados.serializers.area.area_nested_serializer import AreaNestedSerializer
from empleados.serializers.cargo.cargo_nested_serializer import CargoNestedSerializer

class EmpleadoDetailSerializer(serializers.ModelSerializer):

    area = AreaNestedSerializer(
        source="cargo.area",
        read_only=True
    )

    cargo = CargoNestedSerializer(
        read_only=True
    )

    class Meta:
        model = Empleado
        fields = (
            "id",
            "numero_documento",
            "nombre",
            "correo",
            "cargo",
            "area",
            "fecha_ingreso",
            "estado",
        )