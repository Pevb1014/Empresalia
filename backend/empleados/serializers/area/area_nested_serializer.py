from rest_framework import serializers

from empleados.models import Area


class AreaNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = (
            "id",
            "nombre",
        )