<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import DataTable from "@/components/DataTable.vue";
import { adaptHistorialToTable } from "@/adapters/historial.adapter";

const router = useRouter();
const historial = ref([]);
const cargando = ref(true);

const columns = [
  { key: "empleado", label: "Empleado" },
  { key: "tipo", label: "Operación" },
  { key: "fecha", label: "Fecha" }
];

async function cargarHistorial() {
  try {
    cargando.value = true;
    const res = await api.get("historial/");
    historial.value = res.data.results.map(adaptHistorialToTable);
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
</template>