from rest_framework import serializers
from empleados.models.area import Area
from empleados.utils.text import normalizar_nombre

class AreaWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
            "descripcion"
        ]
        read_only_fields = ["id"]

    def validate_nombre(self, value):

        value = normalizar_nombre(value)

        queryset = Area.objects.filter(
            nombre__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un área registrada con este nombre."
            )

        return value