import { createRouter, createWebHistory } from "vue-router";

import homeRoutes from "./routes/home";
import empleadosRoutes from "./routes/empleados";
import areasRoutes from "./routes/areas";
import cargosRoutes from "./routes/cargos";
import historialRoutes from "./routes/historial";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...homeRoutes,
    ...empleadosRoutes,
    ...areasRoutes,
    ...cargosRoutes,
    ...historialRoutes,
  ],
});

export default router;