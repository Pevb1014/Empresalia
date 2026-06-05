import EmpleadosView from "@/views/empleados/EmpleadosView.vue";
import EmpleadoCreateView from "@/views/empleados/EmpleadoCreateView.vue";
import EmpleadoDetailView from "@/views/empleados/EmpleadoDetailView.vue";
import EmpleadoEditView from "@/views/empleados/EmpleadoEditView.vue";

export default [
  {
    path: "/empleados",
    name: "empleados",
    component: EmpleadosView,
  },

  {
    path: "/empleados/nuevo",
    name: "empleado-create",
    component: EmpleadoCreateView,
  },

  {
    path: "/empleados/:id",
    name: "empleado-detail",
    component: EmpleadoDetailView,
    props: true,
  },

  {
    path: "/empleados/:id/editar",
    name: "empleado-edit",
    component: EmpleadoEditView,
    props: true,
  },
];