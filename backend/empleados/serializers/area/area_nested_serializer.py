from rest_framework import serializers

from empleados.models import Area

class AreaNestedSerializer(serializers.ModelSerializer):
    """
    Serializador anidado para una representación ligera del modelo Area.

    Este serializador se utiliza para incluir una representación mínima de un objeto
    `Area` dentro de otros serializadores (anidamiento). Solo expone el `id` y el `nombre`
    del área, lo que es útil para evitar la sobrecarga de datos y la recursividad
    infinita en relaciones complejas, proporcionando solo la información esencial
    para identificar el área.
    """

    class Meta:
        model = Area
        fields = (
            "id",
            "nombre",
        )