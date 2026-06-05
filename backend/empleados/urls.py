from rest_framework.routers import DefaultRouter

from empleados.views import (
    AreaViewSet,
    CargoViewSet,
    EmpleadoViewSet,
    HistorialViewSet,
)

router = DefaultRouter()

router.register(r"areas", AreaViewSet)
router.register(r"cargos", CargoViewSet)

router.register(
    r"empleados",
    EmpleadoViewSet,
    basename="empleado"
)

router.register(
    r"historial",
    HistorialViewSet,
    basename="historial"
)

urlpatterns = router.urls