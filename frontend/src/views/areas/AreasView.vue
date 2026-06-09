<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarAreas, eliminarArea } from "@/api/area.api"; 
import DataTable from "@/components/DataTable.vue";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import { adaptAreaToTable, adaptFormToAreaPayload } from "@/adapters/areas.adapter";

const router = useRouter();
const areas = ref([]);

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
    const res = await listarAreas();
    areas.value = res.data.results.map(adaptAreaToTable);
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

// Lógica de eliminación real conectada al Backend
async function eliminar(item: any) {
  const confirmar = confirm(`¿Estás seguro de que deseas eliminar el área "${item.nombre}"?`);
  
  if (confirmar) {
    try {
      // Ejecuta el método DELETE en Django via tu API modular
      await eliminarArea(item.id);
      
      // Refresca la lista en pantalla tras borrar con éxito
      await cargarAreas(); 
    } catch (error) {
      console.error("Error al eliminar el área:", error);
      alert("No se pudo eliminar el área. Verifica si tiene cargos asociados.");
    }
  }
}
</script>

<template>
  <div class="view-header">
    <h1>Áreas</h1>
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