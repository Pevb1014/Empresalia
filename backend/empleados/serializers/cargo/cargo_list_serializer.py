from rest_framework import serializers
from empleados.models import Cargo


class CargoListSerializer(serializers.ModelSerializer):

    area = serializers.CharField(source="area.nombre", read_only=True)
    
    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
            "area",
        )