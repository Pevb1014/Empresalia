<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarAreas, eliminarArea } from "@/api/area.api"; 
import DataTable from "@/components/DataTable.vue";
import Pagination from "@/components/Pagination.vue";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import ActionModal from "@/components/ActionModal.vue";
import { adaptAreaToTable, adaptFormToAreaPayload } from "@/adapters/areas.adapter";

const router = useRouter();
const areas = ref([]);
const totalItems = ref(0);
const currentPage = ref(1);
const pageSize = 10; // Coincide con el default del back
const procesando = ref(false);
const itemAEliminar = ref<any>(null);
const modal = ref({
  show: false,
  title: "",
  message: "",
  type: "confirm" as "confirm" | "info" | "error"
});

// 1. Definimos la configuración del formulario según el serializer del back
const areaFields: FormField[] = [
  { key: "nombre", label: "Nombre del Área", type: "text", required: true, placeholder: "Ej: Recursos Humanos" },
  { key: "descripcion", label: "Descripción", type: "textarea", placeholder: "Funciones del área..." }
];

const columns = [
  { key: "nombre", label: "Nombre" }
];

// Función centralizada para cargar y refrescar los datos
async function cargarAreas() {
  try {
    const res = await listarAreas({ page: currentPage.value });
    areas.value = res.data.results.map(adaptAreaToTable);
    totalItems.value = res.data.count;
  } catch (error) {
    console.error("Error al obtener las áreas:", error);
  }
}

onMounted(() => {
  cargarAreas();
});

// Navegación a la vista de detalle (donde estará la edición)
function verDetalle(item: any) {
  router.push({ name: "area-detail", params: { id: item.id } });
}

// Navegación directa a edición
function irAEditar(item: any) {
  router.push({ name: "area-edit", params: { id: item.id } });
}

function iniciarEliminacion(item: any) {
  itemAEliminar.value = item;
  modal.value = {
    show: true,
    title: "Confirmar acción",
    message: `¿Seguro que deseas eliminar el área "${item.nombre}"?`,
    type: "confirm"
  };
}

async function ejecutarEliminacion() {
  if (!itemAEliminar.value) return;
  procesando.value = true;
  try {
    await eliminarArea(itemAEliminar.value.id);
    modal.value = {
      show: true,
      title: "Éxito",
      message: "Área eliminada correctamente.",
      type: "info"
    };
    await cargarAreas();
  } catch (error) {
    modal.value = {
      show: true,
      title: "Error",
      message: "No se pudo eliminar el área. Verifica dependencias.",
      type: "error"
    };
  } finally {
    procesando.value = false;
    itemAEliminar.value = null;
  }
}
</script>

<template>
  <div class="view-card">
    <div class="view-header">
      <h1>Áreas Corporativas</h1>
      <button @click="router.push({ name: 'area-create' })" class="btn-nuevo">
        + Nueva Área
      </button>
    </div>

    <DataTable
      :data="areas"
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
      @update:current-page="cargarAreas"
    />
  </div>

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
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .view-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.btn-nuevo { background: #2e7d32; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
.btn-nuevo:hover { background: #1b5e20; }
</style>