from rest_framework import serializers

from empleados.models import Cargo


class CargoNestedSerializer(serializers.ModelSerializer):
    """
    Serializador anidado para una representación mínima del modelo Cargo.

    Se utiliza principalmente dentro de otros serializadores (como AreaDetail)
    para listar los cargos asociados sin incurrir en redundancia de datos
    ni problemas de recursividad.
    """

    class Meta:
        model = Cargo
        fields = (
            "id",
            "nombre",
        )