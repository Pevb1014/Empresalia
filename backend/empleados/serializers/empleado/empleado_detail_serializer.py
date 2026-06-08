from rest_framework import serializers
from empleados.models import Empleado
from empleados.serializers.area.area_nested_serializer import AreaNestedSerializer
from empleados.serializers.cargo.cargo_nested_serializer import CargoNestedSerializer

class EmpleadoDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para la vista detallada de un Empleado.

    Proporciona una representación completa incluyendo la jerarquía organizacional
    (Cargo y Área) mediante serializadores anidados. Se utiliza exclusivamente
    para operaciones de lectura donde se requiere la información descriptiva 
    completa en lugar de solo identificadores.
    """

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