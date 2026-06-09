<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarCargos, eliminarCargo } from "@/api/cargo.api"; 
import DataTable from "@/components/DataTable.vue";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import { adaptCargoToTable } from "@/adapters/cargos.adapter";

const router = useRouter();
const cargos = ref([]);

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
    const res = await listarCargos();
    cargos.value = res.data.results.map(adaptCargoToTable);
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

// Lógica de eliminación real conectada al Backend
async function eliminar(item: any) {
  const confirmar = confirm(`¿Estás seguro de que deseas eliminar el cargo "${item.nombre}"?`);
  
  if (confirmar) {
    try {
      // Ejecuta el método DELETE en Django via tu API modular
      await eliminarCargo(item.id);
      
      // Refresca la lista en pantalla tras borrar con éxito
      await cargarCargos(); 
    } catch (error) {
      console.error("Error al eliminar el cargo:", error);
      alert("No se pudo eliminar el cargo. Verifica si tiene empleados vinculados.");
    }
  }
}
</script>

<template>
  <div class="view-header">
    <h1>Cargos</h1>
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
    @delete="eliminar"
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
</style>