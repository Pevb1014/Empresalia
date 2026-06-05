from rest_framework import serializers

from empleados.serializers.cargo.cargo_nested_serializer import CargoNestedSerializer
from empleados.models import Area


class AreaDetailSerializer(serializers.ModelSerializer):

    cargos = CargoNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
            "descripcion",
            "cargos"
        ]

