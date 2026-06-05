from rest_framework import serializers

from empleados.models import Cargo


class CargoNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
        )