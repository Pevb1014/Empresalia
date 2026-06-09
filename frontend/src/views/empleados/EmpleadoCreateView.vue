<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { crearEmpleado } from "@/api/empleado.api.ts";
import { listarCargos } from "@/api/cargo.api.ts";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import SuccessModal from "@/components/SuccessModal.vue";
import { adaptFormToEmpleadoPayload } from "@/adapters/empleados.adapter";

const router = useRouter();
const cargando = ref(false);
const mostrarExito = ref(false);
const errorMsg = ref("");
const validationErrors = ref<Record<string, string>>({});

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
  validationErrors.value = {};

  try {
    const payload = adaptFormToEmpleadoPayload(formData);
    await crearEmpleado(payload);
    mostrarExito.value = true;
  } catch (error: any) {
    console.error("Error al registrar empleado:", error);
    if (error.response?.data?.errors) {
      error.response.data.errors.forEach((err: any) => {
        validationErrors.value[err.campo] = err.mensaje;
      });
      errorMsg.value = "Existen errores en los datos del empleado.";
    } else {
      const data = error.response?.data;
      errorMsg.value = data?.error || "Error al validar los datos.";
    }
  } finally {
    cargando.value = false;
  }
}

function irAlListado() {
  router.push({ name: "empleados" });
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
      :validation-errors="validationErrors"
      :show-cancel="true"
      submit-label="Registrar"
      @submit="handleFormSubmit"
      @cancel="router.push({ name: 'empleados' })"
    />

    <SuccessModal
      :show="mostrarExito"
      title="¡Empleado Registrado!"
      message="La ficha del nuevo empleado ha sido creada exitosamente."
      @confirm="irAlListado"
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

@media (max-width: 640px) {
  .view-container {
    margin: 1rem;
    padding: 1.5rem;
    max-width: none;
  }
}
</style>