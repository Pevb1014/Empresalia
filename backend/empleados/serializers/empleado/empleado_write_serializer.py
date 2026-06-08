from rest_framework import serializers
from empleados.services.empleado_service import registrar_cambios_empleado, registrar_creacion_empleado
from empleados.models import Empleado, Cargo

class EmpleadoWriteSerializer(serializers.ModelSerializer):

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

        queryset = Empleado.objects.filter(numero_documento__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe un empleado registrado con este número de documento."
            )

        return value
    
    def validate_correo(self, value):

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
        registrar_creacion_empleado(empleado)
        return empleado


    def update(self, instance, validated_data):
        valores_anteriores = {attr: getattr(instance, attr) for attr in validated_data.keys()}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        registrar_cambios_empleado(instance, valores_anteriores, validated_data)

        return instance