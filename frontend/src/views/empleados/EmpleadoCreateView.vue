<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { crearEmpleado } from "@/api/empleado.api.ts";
import { listarCargos } from "@/api/cargo.api.ts";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import { adaptFormToEmpleadoPayload } from "@/adapters/empleados.adapter";

const router = useRouter();
const cargando = ref(false);
const errorMsg = ref("");

const empleadoFields = ref<FormField[]>([
  { key: "nombre", label: "Nombre", type: "text", required: true },
  { key: "numero_documento", label: "Documento de Identidad", type: "text", required: true },
  { key: "correo", label: "Correo Electrónico", type: "email", required: true },
  { key: "fecha_ingreso", label: "Fecha de Ingreso", type: "date", required: true },
  { key: "cargo", label: "Cargo Asignado", type: "select", required: true, options: [] },
  { key: "estado", label: "Estado", type: "select", required: true, options: [
    { value: "ACTIVO", label: "Activo" },
    { value: "INACTIVO", label: "Inactivo" }
  ]},
]);

onMounted(async () => {
  try {
    const res = await listarCargos();
    const cargoSelect = empleadoFields.value.find(f => f.key === "cargo");
    if (cargoSelect) {
      cargoSelect.options = res.data.results.map((c: any) => ({
        value: c.id,
        label: c.nombre
      }));
    }
  } catch (error) {
    console.error("Error al cargar cargos:", error);
    errorMsg.value = "No se pudieron cargar los cargos para el formulario.";
  }
});

async function handleFormSubmit(formData: Record<string, any>) {
  cargando.value = true;
  errorMsg.value = "";

  try {
    const payload = adaptFormToEmpleadoPayload(formData);
    await crearEmpleado(payload);
    router.push({ name: "empleados" });
  } catch (error: any) {
    console.error(error);
    const data = error.response?.data;
    errorMsg.value = data?.error || data?.nombre?.[0] || data?.correo?.[0] || "Error al validar los datos.";
  } finally {
    cargando.value = false;
  }
}
</script>

<template>
  <div class="view-container">
    <header class="view-header">
      <h1>Registrar Nuevo Empleado</h1>
    </header>

    <DynamicForm
      :fields="empleadoFields"
      :loading="cargando"
      :error-msg="errorMsg"
      :show-cancel="true"
      submit-label="Registrar"
      @submit="handleFormSubmit"
      @cancel="router.push({ name: 'empleados' })"
    />
  </div>
</template>

<style scoped>
.view-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.view-header {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.view-header h1 {
  font-size: 1.5rem;
  color: #1a1a1a;
  margin: 0;
}
</style>