from rest_framework import serializers
from empleados.models.area import Area
from empleados.utils.text import normalizar_nombre

class AreaWriteSerializer(serializers.ModelSerializer):
    """
    Serializador para la creación y actualización de un modelo Area.

    Este serializador maneja la lógica de validación y persistencia
    para las operaciones de escritura (crear y actualizar) de objetos Area.
    Incluye validaciones personalizadas para asegurar la unicidad del nombre
    del área.
    """
    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
            "descripcion"
        ]
        read_only_fields = ["id"]
        """
        `read_only_fields` asegura que el campo `id` no pueda ser modificado
        por el cliente, ya que es un identificador generado por el sistema.
        """

    def validate_nombre(self, value):
        """
        Valida que el nombre del área sea único (ignorando mayúsculas/minúsculas).

        Args:
            value (str): El nombre propuesto para el área.

        Raises:
            serializers.ValidationError: Si ya existe un área con el mismo nombre
                                         (ignorando mayúsculas/minúsculas).

        Returns:
            str: El nombre validado.
        """
        value = normalizar_nombre(value)
        
        queryset = Area.objects.filter(nombre__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un área registrada con este nombre."
            )

        return value