from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from empleados.models import Empleado
from empleados.serializers.empleado.empleado_list_serializer import EmpleadoListSerializer
from empleados.serializers.empleado.empleado_detail_serializer import EmpleadoDetailSerializer
from empleados.serializers.empleado.empleado_write_serializer import EmpleadoWriteSerializer

class EmpleadoViewSet(ModelViewSet):
    """
    Controlador integral del Personal (Empleados).

    Procesa el registro, consulta y actualización de los datos maestros 
    de los trabajadores de la organización. Cuenta con capacidades robustas de 
    búsqueda por coincidencias, ordenamiento y filtrado por dependencias estructuradas.
    """

    def get_queryset(self):
        return (
            Empleado.objects
            .select_related(
                "cargo",
                "cargo__area"
            )
        )

    def get_serializer_class(self):
        if self.action == "list":
            return EmpleadoListSerializer

        if self.action == "retrieve":
            return EmpleadoDetailSerializer

        return EmpleadoWriteSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = {
        "estado": ["exact"],
        "cargo": ["exact"],
        "cargo__area": ["exact"],
    }

    search_fields = ["nombre", "numero_documento", "correo"]
    ordering_fields = ["nombre", "fecha_ingreso", "correo"]
    ordering = ["nombre"]