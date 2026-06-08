from rest_framework import serializers

from empleados.serializers.cargo.cargo_nested_serializer import CargoNestedSerializer
from empleados.models import Area

class AreaDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para la representación detallada de un modelo Area.

    Este serializador se utiliza para mostrar todos los campos de un área,
    incluyendo su descripción y una lista anidada de los cargos asociados.
    Es ideal para vistas de detalle donde se requiere información completa
    y las relaciones directas.
    """

    cargos = CargoNestedSerializer(many=True, read_only=True)
    """
    Campo anidado que representa los cargos asociados a esta área.
    Utiliza `CargoNestedSerializer` para una representación ligera de cada cargo
    (solo `id` y `nombre`).
    `many=True` indica que puede haber múltiples cargos.
    `read_only=True` asegura que los cargos no se puedan crear o actualizar
    directamente a través de este serializador de área.
    """

    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
            "descripcion",
            "cargos"
        ]
