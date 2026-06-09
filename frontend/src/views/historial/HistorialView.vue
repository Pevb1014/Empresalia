<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarHistorial } from "@/api/historial.api";
import DataTable from "@/components/DataTable.vue";
import Pagination from "@/components/Pagination.vue";
import { adaptHistorialToTable } from "@/adapters/historial.adapter";

const router = useRouter();
const historial = ref([]);
const cargando = ref(true);
const totalItems = ref(0);
const currentPage = ref(1);
const pageSize = 10;

const columns = [
  { key: "empleado", label: "Empleado" },
  { key: "tipo", label: "Operación" },
  { key: "fecha", label: "Fecha" }
];

async function cargarHistorial() {
  try {
    cargando.value = true;
    const res = await listarHistorial({ page: currentPage.value });
    historial.value = res.data.results.map(adaptHistorialToTable);
    totalItems.value = res.data.count;
  } catch (error) {
    console.error("Error al cargar historial:", error);
  } finally {
    cargando.value = false;
  }
}

onMounted(cargarHistorial);

function verDetalle(item: any) {
  router.push({ name: "historial-detail", params: { id: item.id } });
}
</script>

<template>
  <h1>Historial</h1>

  <div v-if="cargando">Cargando bitácoras...</div>
  <DataTable v-else
    :data="historial"
    :columns="columns"
    :show-edit="false"
    :show-delete="false"
    @detail="verDetalle"
  />

  <Pagination
    :total-items="totalItems"
    :page-size="pageSize"
    v-model:current-page="currentPage"
    @update:current-page="cargarHistorial"
  />
</template>

<style scoped>
@media (max-width: 640px) {
  h1 { font-size: 1.5rem; margin-bottom: 1rem; }
}
</style>