from rest_framework import serializers
from empleados.services.empleado_service import registrar_cambios_empleado, registrar_creacion_empleado
from empleados.models import Empleado, Cargo

class EmpleadoWriteSerializer(serializers.ModelSerializer):

    cargo_id = serializers.PrimaryKeyRelatedField(
        queryset=Cargo.objects.all(),
        source="cargo",
        write_only=True
    )

    class Meta:
        model = Empleado
        fields = [
            "id",
            "numero_documento",
            "nombre",
            "correo",
            "fecha_ingreso",
            "estado",
            "cargo_id",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        empleado = Empleado.objects.create(**validated_data)
        registrar_creacion_empleado(empleado)
        return empleado

    def update(self, instance, validated_data):
        valores_anteriores = {attr: getattr(instance, attr) for attr in validated_data.keys()}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        registrar_cambios_empleado(instance, valores_anteriores, validated_data)

        return instance