from rest_framework import serializers
from empleados.models import Cargo, Area


class CargoWriteSerializer(serializers.ModelSerializer):

    area_id = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(),
        source="area"
    )

    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
            "descripcion",
            "area_id",
        )
        read_only_fields = ("id",)


    def validate_nombre(self, value):

        queryset = Cargo.objects.filter(nombre__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un cargo con este nombre."
            )

        return value