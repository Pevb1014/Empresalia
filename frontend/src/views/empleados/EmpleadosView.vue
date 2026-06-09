<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarEmpleados, eliminarEmpleado } from "@/api/empleado.api";
import DataTable from "@/components/DataTable.vue";
import Pagination from "@/components/Pagination.vue";
import { type FormField } from "@/components/DynamicForm.vue";
import ActionModal from "@/components/ActionModal.vue";
import { adaptEmpleadoToTable } from "@/adapters/empleados.adapter";

const router = useRouter();
const empleados = ref([]);
const totalItems = ref(0);
const currentPage = ref(1);
const pageSize = 10;
const procesando = ref(false);
const itemAEliminar = ref<any>(null);
const modal = ref({
  show: false,
  title: "",
  message: "",
  type: "confirm" as "confirm" | "info" | "error"
});

// 1. Configuración del formulario (útil para futuras acciones de creación/edición rápida)
const empleadoFields: FormField[] = [
  { key: "nombre", label: "Nombre", type: "text", required: true },
  { key: "numero_documento", label: "Número de Documento", type: "text", required: true },
  { key: "correo", label: "Correo Electrónico", type: "email", required: true },
  { key: "fecha_ingreso", label: "Fecha de Ingreso", type: "date", required: true },
  { key: "estado", label: "Estado", type: "select", required: true, options: [
    { value: "ACTIVO", label: "Activo" },
    { value: "INACTIVO", label: "Inactivo" }
  ]},
  { key: "cargo", label: "Cargo", type: "select", required: true }
];

const columns = [
  { key: "nombre", label: "Nombre" },
  { key: "cargo", label: "Cargo" },
  { key: "area", label: "Área" }
];

// Función centralizada para cargar y refrescar los datos
async function cargarEmpleados() {
  try {
    const res = await listarEmpleados({ page: currentPage.value });
    empleados.value = res.data.results.map(adaptEmpleadoToTable);
    totalItems.value = res.data.count;
  } catch (error) {
    console.error("Error al obtener empleados:", error);
  }
}

onMounted(() => {
  cargarEmpleados();
});

// Navegación a la vista de detalle
function verDetalle(item: any) {
  router.push({ name: "empleado-detail", params: { id: item.id } });
}

// Navegación directa a edición
function irAEditar(item: any) {
  router.push({ name: "empleado-edit", params: { id: item.id } });
}

function iniciarEliminacion(item: any) {
  itemAEliminar.value = item;
  modal.value = {
    show: true,
    title: "Confirmar acción",
    message: `¿Estás seguro de que deseas eliminar al empleado "${item.nombre}"?`,
    type: "confirm"
  };
}

async function ejecutarEliminacion() {
  if (!itemAEliminar.value) return;
  procesando.value = true;
  try {
    await eliminarEmpleado(itemAEliminar.value.id);
    modal.value = {
      show: true,
      title: "Éxito",
      message: "Empleado eliminado correctamente.",
      type: "info"
    };
    await cargarEmpleados();
  } catch (error) {
    modal.value = {
      show: true,
      title: "Error",
      message: "No se pudo eliminar el empleado.",
      type: "error"
    };
  } finally {
    procesando.value = false;
    itemAEliminar.value = null;
  }
}
</script>

<template>
  <div class="view-header">
    <h1>Empleados</h1>
    <button @click="router.push({ name: 'empleado-create' })" class="btn-nuevo">
      + Registrar Empleado
    </button>
  </div>

  <DataTable
    :data="empleados"
    :columns="columns"
    :show-edit="true"
    :show-delete="true"
    @detail="verDetalle"
    @edit="irAEditar"
    @delete="iniciarEliminacion"
  />

  <Pagination
    :total-items="totalItems"
    :page-size="pageSize"
    v-model:current-page="currentPage"
    @update:current-page="cargarEmpleados"
  />

  <ActionModal
    :show="modal.show"
    :title="modal.title"
    :message="modal.message"
    :type="modal.type"
    :loading="procesando"
    @confirm="ejecutarEliminacion"
    @close="modal.show = false"
  />
</template>

<style scoped>
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-nuevo { background: #2e7d32; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
.btn-nuevo:hover { background: #1b5e20; }

@media (max-width: 640px) {
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .btn-nuevo { width: 100%; text-align: center; }
}
</style>