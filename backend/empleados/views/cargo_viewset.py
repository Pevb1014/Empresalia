from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db.models.deletion import ProtectedError
from rest_framework.response import Response
from empleados.models import Cargo
from empleados.serializers.cargo.cargo_list_serializer import CargoListSerializer
from empleados.serializers.cargo.cargo_detail_serializer import CargoDetailSerializer
from empleados.serializers.cargo.cargo_write_serializer import CargoWriteSerializer


class CargoViewSet(ModelViewSet):
    """
    Controlador para la administración de Cargos.

    Permite crear, listar, actualizar y eliminar los puestos u ocupaciones
    laborales de la empresa, vinculándolos a su respectiva área jerárquica.
    """

    queryset = Cargo.objects.all()

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre"]

    def get_queryset(self):
        """
        Recupera los cargos con optimización de relaciones foráneas.

        Utiliza select_related para obtener el área en la misma consulta y,
        específicamente en la acción 'retrieve', prefetch_related para los
        empleados asignados al cargo.
        """
        queryset = super().get_queryset().select_related("area")
        if self.action == "retrieve":
            return queryset.prefetch_related("empleados")
        return queryset

    def get_serializer_class(self):
        """
        Selecciona la clase del serializador basándose en la acción del ViewSet.

        Permite diferenciar la información retornada en listados, detalles
        completos o procesos de persistencia (escritura).
        """

        if self.action == "list":
            return CargoListSerializer

        if self.action == "retrieve":
            return CargoDetailSerializer

        return CargoWriteSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Elimina un cargo del sistema.

        Verifica explícitamente en el ORM si existen empleados asignados a este
        cargo antes de proceder. En caso afirmativo, interrumpe la eliminación
        para preservar la integridad del historial del personal.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    "error": "No se puede eliminar el cargo porque tiene empleados asociados."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
