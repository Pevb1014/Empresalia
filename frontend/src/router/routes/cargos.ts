import CargosView from "@/views/cargos/CargosView.vue";
import CargoCreateView from "@/views/cargos/CargoCreateView.vue";
import CargoDetailView from "@/views/cargos/CargoDetailView.vue";
import CargoEditView from "@/views/cargos/CargoEditView.vue";

export default [
  {
    path: "/cargos",
    name: "cargos",
    component: CargosView,
  },

  {
    path: "/cargos/nuevo",
    name: "cargo-create",
    component: CargoCreateView,
  },

  {
    path: "/cargos/:id",
    name: "cargo-detail",
    component: CargoDetailView,
    props: true,
  },

  {
    path: "/cargos/:id/editar",
    name: "cargo-edit",
    component: CargoEditView,
    props: true,
  },
];