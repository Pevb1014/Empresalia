from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from empleados.models import HistorialCambio
from empleados.serializers.historial.historial_list_serializer import HistorialListSerializer
from empleados.serializers.historial.historial_detail_serializer import HistorialDetailSerializer


class HistorialViewSet(ModelViewSet):
    """
    Controlador de Solo Lectura para Auditoría del Sistema.

    Expone las bitácoras automáticas de los cambios sufridos en las fichas de 
    los empleados. Permite trazar qué campos variaron, cuándo sucedió, 
    y cuáles eran los valores anteriores y nuevos correspondientes.
    """

    http_method_names = ["get"]

    def get_queryset(self):
        return (
            HistorialCambio.objects
            .select_related("empleado__cargo__area")
            .all()
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return HistorialDetailSerializer

        return HistorialListSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "empleado": ["exact"],
        "tipo_cambio": ["exact"],
        "empleado__cargo": ["exact"],
        "empleado__cargo__area": ["exact"],
    }
    ordering_fields = ["fecha_cambio"]
    ordering = ["-fecha_cambio"]