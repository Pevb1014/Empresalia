<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarCargos, eliminarCargo } from "@/api/cargoApi";
import DataTable from "@/components/DataTable.vue";
import { adaptCargo } from "@/adapters/cargos.adapter";

const router = useRouter();
const cargos = ref([]);

const columns = [
  { key: "nombre", label: "Nombre del Cargo" },
  { key: "area.nombre", label: "Área Asociada" }
];

async function cargarCargos() {
  try {
    const res = await listarCargos();
    console.log("=== RESPUESTA RAW DE DJANGO (LISTA DE CARGOS) ===");
    console.log(res.data);
    cargos.value = res.data.results.map(adaptCargo);
  } catch (error) {
    console.error("Error al obtener los cargos:", error);
  }
}

onMounted(() => {
  cargarCargos();
});

function verDetalle(item: any) {
  router.push({ name: "cargo-detail", params: { id: item.id } });
}

async function eliminar(item: any) {
  const confirmar = confirm(`¿Deseas eliminar el cargo "${item.nombre}"?`);
  if (confirmar) {
    try {
      await eliminarCargo(item.id);
      await cargarCargos();
    } catch (error) {
      console.error("Error al eliminar el cargo:", error);
      alert("No se pudo eliminar el cargo. Verifica si tiene empleados vinculados.");
    }
  }
}
</script>

<template>
  <h1>Cargos</h1>

  <DataTable
    :data="cargos"
    :columns="columns"
    :show-edit="false"
    :show-delete="true"
    @detail="verDetalle"
    @delete="eliminar"
  />
</template>