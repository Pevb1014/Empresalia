import AreasView from "@/views/areas/AreasView.vue";
import AreaCreateView from "@/views/areas/AreaCreateView.vue";
import AreaDetailView from "@/views/areas/AreaDetailView.vue";
import AreaEditView from "@/views/areas/AreaEditView.vue";

export default [
  {
    path: "/areas",
    name: "areas",
    component: AreasView,
  },

  {
    path: "/areas/nueva",
    name: "area-create",
    component: AreaCreateView,
  },

  {
    path: "/areas/:id",
    name: "area-detail",
    component: AreaDetailView,
    props: true,
  },

  {
    path: "/areas/:id/editar",
    name: "area-edit",
    component: AreaEditView,
    props: true,
  },
];