<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { crearCargo } from "@/api/cargo.api.ts";
import { listarAreas } from "@/api/area.api.ts";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import { adaptFormToCargoPayload } from "@/adapters/cargos.adapter";

const router = useRouter();
const cargando = ref(false);
const errorMsg = ref("");

const cargoFields = ref<FormField[]>([
  {
    key: "nombre",
    label: "Nombre del Cargo",
    type: "text",
    placeholder: "Ej. Desarrollador Frontend, Analista...",
    required: true,
  },
  {
    key: "area",
    label: "Área de la Empresa",
    type: "select",
    placeholder: "Seleccione el área de pertenencia",
    required: true,
    options: [], 
  },
  {
    key: "descripcion",
    label: "Descripción",
    type: "textarea",
    placeholder: "Escriba las funciones o responsabilidades (opcional)...",
    required: false,
  },
]);

onMounted(async () => {
  try {
    const res = await listarAreas();
    const areaSelect = cargoFields.value.find(f => f.key === "area");
    if (areaSelect) {
      areaSelect.options = res.data.results.map((area: any) => ({
        value: area.id,
        label: area.nombre,
      }));
    }
  } catch (error) {
    console.error("Error al cargar las áreas para el formulario:", error);
    errorMsg.value = "No se pudieron cargar las áreas. Intente recargar la página.";
  }
});

async function handleFormSubmit(formData: Record<string, any>) {
  cargando.value = true;
  errorMsg.value = "";

  try {
    const payload = adaptFormToCargoPayload(formData);
    await crearCargo(payload);
    router.push({ name: "cargos" });
  } catch (error: any) {
    console.error(error);
    if (error.response?.data) {
      const data = error.response.data;
      errorMsg.value = data.error || data.nombre?.[0] || "Ocurrió un error al validar los datos en el servidor.";
    } else {
      errorMsg.value = "Error de comunicación con el servidor.";
    }
  } finally {
    cargando.value = false;
  }
}
</script>

<template>
  <div class="view-container">
    <header class="view-header">
      <h1>Crear Nuevo Cargo</h1>
    </header>

    <DynamicForm
      :fields="cargoFields"
      :loading="cargando"
      :error-msg="errorMsg"
      :show-cancel="true"
      submit-label="Guardar Cargo"
      @submit="handleFormSubmit"
      @cancel="router.push({ name: 'cargos' })"
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