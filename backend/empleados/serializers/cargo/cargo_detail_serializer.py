from rest_framework import serializers
from empleados.models import Cargo
from empleados.serializers.area.area_nested_serializer import AreaNestedSerializer


class CargoDetailSerializer(serializers.ModelSerializer):

    area = AreaNestedSerializer(read_only=True)

    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
            "descripcion",
            "area",
        )