<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
// Importamos listar y eliminar de tu capa de API
import { listarAreas, eliminarArea } from "@/api/areaApi"; 
import DataTable from "@/components/DataTable.vue";
import { adaptArea } from "@/adapters/areas.adapter";

const router = useRouter();
const areas = ref([]);

const columns = [
  { key: "nombre", label: "Nombre" }
];

// Función centralizada para cargar y refrescar los datos
async function cargarAreas() {
  try {
    const res = await listarAreas();
    areas.value = res.data.results.map(adaptArea);
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
  <h1>Áreas</h1>

  <DataTable
    :data="areas"
    :columns="columns"
    :show-edit="false"
    :show-delete="true"
    @detail="verDetalle"
    @delete="eliminar"
  />
</template>