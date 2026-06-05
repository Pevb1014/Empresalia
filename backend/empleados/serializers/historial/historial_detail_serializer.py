from rest_framework import serializers
from empleados.models import HistorialCambio
from empleados.serializers.empleado.empleado_nested_serializer import EmpleadoNestedSerializer


class HistorialDetailSerializer(serializers.ModelSerializer):

    empleado = EmpleadoNestedSerializer(read_only=True)

    class Meta:
        model = HistorialCambio
        fields = "__all__"