<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { crearEmpleado } from "@/api/empleadoApi";
import { listarCargos } from "@/api/cargoApi";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import { adaptFormToEmpleadoPayload } from "@/adapters/empleados.adapter";

const router = useRouter();
const cargando = ref(false);
const errorMsg = ref("");

const empleadoFields = ref<FormField[]>([
  { key: "nombre", label: "Nombre", type: "text", required: true },
  { key: "apellido", label: "Apellido", type: "text", required: true },
  { key: "email", label: "Correo Electrónico", type: "email", required: true },
  { key: "cargo", label: "Cargo Asignado", type: "select", required: true, options: [] }
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
    errorMsg.value = error.response?.data?.email?.[0] || "Error al guardar el empleado.";
  } finally {
    cargando.value = false;
  }
}
</script>

<template>
  <div class="form-container">
    <h1>Registrar Empleado</h1>
    <hr />
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
.form-container { max-width: 600px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
hr { margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eee; }
</style>