from rest_framework import serializers

from empleados.models.area import Area

class AreaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
        ]