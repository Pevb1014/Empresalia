from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from empleados.models import Empleado
from empleados.serializers.empleado.empleado_list_serializer import (
    EmpleadoListSerializer,
)
from empleados.serializers.empleado.empleado_detail_serializer import (
    EmpleadoDetailSerializer,
)
from empleados.serializers.empleado.empleado_write_serializer import (
    EmpleadoWriteSerializer,
)


class EmpleadoViewSet(ModelViewSet):
    """
    Controlador integral del Personal (Empleados).

    Procesa el registro, consulta y actualización de los datos maestros
    de los trabajadores de la organización. Cuenta con capacidades robustas de
    búsqueda por coincidencias, ordenamiento y filtrado por dependencias estructuradas.
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = {
        "estado": ["exact"],
        "cargo": ["exact"],
        "cargo__area": ["exact"],
    }

    search_fields = ["nombre", "numero_documento", "correo"]
    ordering_fields = ["nombre", "fecha_ingreso", "correo"]
    ordering = ["nombre"]

    def get_queryset(self):
        """
        Construye la consulta para empleados con carga anticipada de relaciones.

        Optimiza la obtención del cargo y el área asociada mediante
        select_related. En la acción 'retrieve', incorpora prefetch_related
        para cargar el historial de cambios asociado de forma eficiente.
        """
        queryset = Empleado.objects.select_related("cargo", "cargo__area")
        if self.action == "retrieve":
            return queryset.prefetch_related("historial")
        return queryset

    def get_serializer_class(self):
        """
        Retorna la clase serializadora correspondiente a la acción actual.

        Distingue entre la vista de lista (resumida), la vista de detalle
        (expandida con área y cargo) y las operaciones de escritura.
        """
        if self.action == "list":
            return EmpleadoListSerializer

        if self.action == "retrieve":
            return EmpleadoDetailSerializer

        return EmpleadoWriteSerializer
