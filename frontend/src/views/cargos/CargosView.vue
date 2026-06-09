<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarCargos, eliminarCargo } from "@/api/cargo.api"; 
import DataTable from "@/components/DataTable.vue";
import Pagination from "@/components/Pagination.vue";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import ActionModal from "@/components/ActionModal.vue";
import { adaptCargoToTable } from "@/adapters/cargos.adapter";

const router = useRouter();
const cargos = ref([]);
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

// 1. Definimos la configuración del formulario según el serializer del back
const cargoFields: FormField[] = [
  { key: "nombre", label: "Nombre del Cargo", type: "text", required: true, placeholder: "Ej: Analista de Sistemas" },
  { key: "descripcion", label: "Descripción", type: "textarea", placeholder: "Responsabilidades del cargo..." },
  { key: "area", label: "Área", type: "select", required: true }
];

const columns = [
  { key: "nombre", label: "Nombre del Cargo" },
  { key: "area", label: "Área Asociada" }
];

// Función centralizada para cargar y refrescar los datos
async function cargarCargos() {
  try {
    const res = await listarCargos({ page: currentPage.value });
    cargos.value = res.data.results.map(adaptCargoToTable);
    totalItems.value = res.data.count;
  } catch (error) {
    console.error("Error al obtener los cargos:", error);
  }
}

onMounted(() => {
  cargarCargos();
});

// Navegación a la vista de detalle (donde estará la edición)
function verDetalle(item: any) {
  router.push({ name: "cargo-detail", params: { id: item.id } });
}

// Navegación directa a edición
function irAEditar(item: any) {
  router.push({ name: "cargo-edit", params: { id: item.id } });
}

function iniciarEliminacion(item: any) {
  itemAEliminar.value = item;
  modal.value = {
    show: true,
    title: "Confirmar acción",
    message: `¿Estás seguro de que deseas eliminar el cargo "${item.nombre}"?`,
    type: "confirm"
  };
}

async function ejecutarEliminacion() {
  if (!itemAEliminar.value) return;
  procesando.value = true;
  try {
    await eliminarCargo(itemAEliminar.value.id);
    modal.value = {
      show: true,
      title: "Éxito",
      message: "Cargo eliminado correctamente.",
      type: "info"
    };
    await cargarCargos();
  } catch (error) {
    modal.value = {
      show: true,
      title: "Error",
      message: "No se pudo eliminar el cargo. Verifica si tiene empleados vinculados.",
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
      <h1>Cargos Institucionales</h1>
      <button @click="router.push({ name: 'cargo-create' })" class="btn-nuevo">
        + Nuevo Cargo
      </button>
    </div>

    <DataTable
      :data="cargos"
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
      @update:current-page="cargarCargos"
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
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-nuevo { background: #2e7d32; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
.btn-nuevo:hover { background: #1b5e20; }

@media (max-width: 600px) {
  .view-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    text-align: center;
  }
  .btn-nuevo { width: 100%; }
}
</style>