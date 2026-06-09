from rest_framework import serializers
from empleados.models import Cargo, Empleado
from empleados.serializers.area.area_nested_serializer import AreaNestedSerializer

class EmpleadoNestedSerializer(serializers.ModelSerializer):
    """
    Representación ligera de un empleado para relaciones anidadas.
    """
    class Meta:
        model = Empleado
        fields = ("id", "nombre")

class CargoDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para la representación detallada de un modelo Cargo.

    Muestra todos los atributos del cargo, incluyendo la información
    completa del área a la que pertenece mediante un serializador anidado.
    """

    area = AreaNestedSerializer(read_only=True)
    """
    Representación anidada del área asociada.
    
    Utiliza `AreaNestedSerializer` para incluir el id y nombre del área.
    Es de solo lectura ya que el área se asigna mediante su ID en 
    operaciones de escritura.
    """

    empleados = EmpleadoNestedSerializer(many=True, read_only=True)
    """
    Lista de empleados que tienen asignado este cargo.
    Aprovecha el prefetch_related del ViewSet para evitar consultas N+1.
    """

    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
            "descripcion",
            "area",
            "empleados",
        )