from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from empleados.models import HistorialCambio
from empleados.serializers.historial.historial_list_serializer import (
    HistorialListSerializer,
)
from empleados.serializers.historial.historial_detail_serializer import (
    HistorialDetailSerializer,
)


class HistorialViewSet(ModelViewSet):
    """
    Controlador de Solo Lectura para Auditoría del Sistema.

    Expone las bitácoras automáticas de los cambios sufridos en las fichas de
    los empleados. Permite trazar qué campos variaron, cuándo sucedió,
    y cuáles eran los valores anteriores y nuevos correspondientes.
    """

    http_method_names = ["get"]

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = {
        "empleado": ["exact"],
        "tipo_cambio": ["exact"],
        "empleado__cargo": ["exact"],
        "empleado__cargo__area": ["exact"],
    }
    
    ordering_fields = ["fecha_cambio"]
    ordering = ["-fecha_cambio"]

    def get_queryset(self):
        """
        Obtiene los registros de auditoría optimizando las relaciones jerárquicas.

        Realiza la carga de empleados, cargos y áreas en una sola consulta SQL
        para facilitar la trazabilidad completa del cambio sin degradar
        el rendimiento.
        """
        return HistorialCambio.objects.select_related("empleado__cargo__area").all()

    def get_serializer_class(self):
        """
        Determina el serializador para los registros de historial.

        Asigna un serializador detallado para la acción 'retrieve' y uno
        estándar para la navegación en listas.
        """
        if self.action == "retrieve":
            return HistorialDetailSerializer

        return HistorialListSerializer
