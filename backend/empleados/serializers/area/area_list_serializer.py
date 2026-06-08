from rest_framework import serializers

from empleados.models.area import Area

class AreaListSerializer(serializers.ModelSerializer):
    """
    Serializador para la representación de lista de un modelo Area.

    Este serializador proporciona una vista concisa de un área,
    incluyendo solo su identificador y nombre. Es adecuado para
    listados o selecciones donde no se necesita información detallada.
    """

    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
        ]