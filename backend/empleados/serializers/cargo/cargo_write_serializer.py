from rest_framework import serializers
from empleados.utils.text import normalizar_nombre
from empleados.models import Cargo, Area


class CargoWriteSerializer(serializers.ModelSerializer):
    """
    Serializador encargado de la creación y actualización de registros de Cargo.

    Incluye lógica de validación personalizada para asegurar la integridad de los datos
    y la unicidad de los nombres tras la normalización de texto.
    """

    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    """
    Campo para vincular el cargo a un área mediante su Identificador (UUID).
    Valida que el área seleccionada exista previamente en el sistema.
    """

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
        """
        Valida y normaliza el nombre del cargo.

        Asegura que no existan duplicados (sin distinguir mayúsculas/minúsculas)
        después de aplicar la normalización. Si se está realizando una 
        actualización, excluye al registro actual de la validación.
        """

        value = normalizar_nombre(value)
        queryset = Cargo.objects.filter(nombre__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un cargo registrado con este nombre."
            )

        return value