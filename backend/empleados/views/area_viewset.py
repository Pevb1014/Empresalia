from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response

from empleados.models import Area
from empleados.serializers.area.area_detail_serializer import AreaDetailSerializer
from empleados.serializers.area.area_list_serializer import AreaListSerializer
from empleados.serializers.area.area_write_serializer import AreaWriteSerializer


class AreaViewSet(ModelViewSet):
    """
    Controlador para la gestión de Áreas Corporativas.

    Ofrece operaciones completas (CRUD) para administrar los departamentos
     u organizaciones estructurales de la empresa.
    """

    queryset = Area.objects.all()

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre"]

    def get_queryset(self):
        """
        Obtiene el conjunto de datos base para las Áreas.

        Aplica optimizaciones de prefetch_related en la acción 'retrieve' para
        cargar eficientemente los cargos y sus empleados asociados, evitando
        múltiples consultas a la base de datos (problema N+1).
        """
        queryset = super().get_queryset()
        if self.action == "retrieve":
            return queryset.prefetch_related("cargos__empleados")
        return queryset

    def get_serializer_class(self):
        """
        Determina qué serializador utilizar según la acción solicitada.

        - 'list': AreaListSerializer (resumen simplificado).
        - 'retrieve': AreaDetailSerializer (detalle completo con cargos).
        - Otros: AreaWriteSerializer (creación y actualización).
        """
        if self.action == "list":
            return AreaListSerializer

        if self.action == "retrieve":
            return AreaDetailSerializer

        return AreaWriteSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Elimina un área específica del sistema.

        Valida mediante restricciones de base de datos que el área no contenga
        cargos dependientes o empleados activos. Si existen dependencias,
        revierte la operación y retorna un error de protección.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    "error": "No se puede eliminar el área porque tiene cargos o empleados asociados."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
