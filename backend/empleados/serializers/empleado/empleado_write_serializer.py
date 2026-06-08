from rest_framework import serializers
from empleados.services.empleado_service import auditar_creacion_empleado, auditar_actualizacion_empleado
from empleados.models.cargo import Cargo
from empleados.models.empleado import Empleado
from empleados.utils.text import normalizar_documento, normalizar_email

class EmpleadoWriteSerializer(serializers.ModelSerializer):
    """
    Serializador para operaciones de escritura en el modelo Empleado.

    Incluye lógica de normalización de datos (email y documento), validaciones
    de unicidad personalizadas y la integración con el servicio de historial
    para auditar creaciones y modificaciones de registros.
    """

    cargo = serializers.PrimaryKeyRelatedField(
        queryset=Cargo.objects.all(),
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
            "cargo",
        ]
        read_only_fields = ["id"]

    def validate_numero_documento(self, value):

        value = normalizar_documento(value)
        queryset = Empleado.objects.filter(numero_documento__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un empleado registrado con este número de documento."
            )

        return value
    
    def validate_correo(self, value):

        value = normalizar_email(value)
        queryset = Empleado.objects.filter(correo__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un empleado registrado con este correo electrónico."
            )

        return value


    def create(self, validated_data):
        empleado = Empleado.objects.create(**validated_data)
        auditar_creacion_empleado(empleado)
        return empleado


    def update(self, instance, validated_data):
        valores_anteriores = {attr: getattr(instance, attr) for attr in validated_data.keys()}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        auditar_actualizacion_empleado(instance, valores_anteriores, validated_data)

        return instance