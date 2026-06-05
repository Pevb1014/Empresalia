<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listarEmpleados, eliminarEmpleado } from "@/api/empleadoApi";
import DataTable from "@/components/DataTable.vue";
import { adaptEmpleado } from "@/adapters/empleados.adapter";

const router = useRouter();
const empleados = ref([]);

const columns = [
  { key: "nombre", label: "Nombre" },
  { key: "apellido", label: "Apellido" },
  { key: "email", label: "Correo Electrónico" },
  { key: "cargo.nombre", label: "Cargo" } // Resuelto por el reduce de tu DataTable
];

async function cargarEmpleados() {
  try {
    const res = await listarEmpleados();
    empleados.value = res.data.results.map(adaptEmpleado);
  } catch (error) {
    console.error("Error al obtener empleados:", error);
  }
}

onMounted(() => {
  cargarEmpleados();
});

function verDetalle(item: any) {
  router.push({ name: "empleado-detail", params: { id: item.id } });
}

async function eliminar(item: any) {
  const confirmar = confirm(`¿Deseas eliminar a ${item.nombre} ${item.apellido}?`);
  if (confirmar) {
    try {
      await eliminarEmpleado(item.id);
      await cargarEmpleados();
    } catch (error) {
      console.error("Error al eliminar:", error);
      alert("No se pudo eliminar el empleado.");
    }
  }
}
</script>

<template>
  <h1>Empleados</h1>

  <DataTable
    :data="empleados"
    :columns="columns"
    :show-edit="false"
    :show-delete="true"
    @detail="verDetalle"
    @delete="eliminar"
  />
</template>