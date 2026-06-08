from rest_framework import serializers
from empleados.models import Cargo, Area


class CargoWriteSerializer(serializers.ModelSerializer):

    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())

    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
            "descripcion",
            "area",
        )
        read_only_fields = ("id",)


    def validate_nombre(self, value):

        queryset = Cargo.objects.filter(nombre__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un cargo registrado con este nombre."
            )

        return value