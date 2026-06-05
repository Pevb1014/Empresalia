<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "@/api/axios";
import DataTable from "@/components/DataTable.vue";
import { adaptHistorial } from "@/adapters/historial.adapter";

const historial = ref([]);

const columns = [
  { key: "empleado", label: "Empleado" },
  { key: "accion", label: "Acción" },
  { key: "fecha", label: "Fecha" }
];

onMounted(async () => {
  const res = await api.get("historial/");

  console.log("RAW HISTORIAL:", res.data);

  historial.value = res.data.results.map(adaptHistorial);

  console.log("ADAPTED HISTORIAL:", historial.value);
});

function editar(item: any) {
  console.log("Editar historial:", item);
}

function eliminar(item: any) {
  console.log("Eliminar historial:", item);
}
</script>

<template>
  <h1>Historial</h1>

  <DataTable
    :data="historial"
    :columns="columns"
    @edit="editar"
    @delete="eliminar"
  />
</template>