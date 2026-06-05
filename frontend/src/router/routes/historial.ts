import HistorialView from "@/views/historial/HistorialView.vue";
import HistorialDetailView from "@/views/historial/HistorialDetailView.vue";

export default [
  {
    path: "/historial",
    name: "historial",
    component: HistorialView,
  },

  {
    path: "/historial/:id",
    name: "historial-detail",
    component: HistorialDetailView,
    props: true,
  },
];