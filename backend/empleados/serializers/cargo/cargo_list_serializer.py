from rest_framework import serializers
from empleados.models import Cargo


class CargoListSerializer(serializers.ModelSerializer):
    """
    Serializador optimizado para listados de Cargos.

    Provee la información mínima necesaria para visualización en tablas,
    incluyendo el nombre del área de forma directa para evitar anidamientos innecesarios.
    """

    area = serializers.CharField(source="area.nombre", read_only=True)
    """
    Nombre del área a la que pertenece el cargo (obtenido mediante la relación area).
    """
    
    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
            "area",
        )