<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { crearArea } from "@/api/area.api";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import SuccessModal from "@/components/SuccessModal.vue";
import { adaptFormToAreaPayload } from "@/adapters/areas.adapter";

const router = useRouter();
const cargando = ref(false);
const mostrarExito = ref(false);
const errorMsg = ref("");
const validationErrors = ref<Record<string, string>>({});

// 1. Configuración de los campos que el formulario dinámico renderizará
const areaFields: FormField[] = [
  {
    key: "nombre",
    label: "Nombre del Área",
    type: "text",
    placeholder: "Ej. Tecnología, Operaciones, Gestión Humana...",
    required: true,
  },
  {
    key: "descripcion",
    label: "Descripción",
    type: "textarea",
    placeholder: "Describe brevemente las funciones o el propósito de esta área...",
  },
];

// 2. Procesamiento del envío de datos
async function handleFormSubmit(formData: Record<string, any>) {
  cargando.value = true;
  errorMsg.value = "";
  validationErrors.value = {};

  try {
    // Pasamos los datos recolectados por el adaptador antes de tocar la API
    const payload = adaptFormToAreaPayload(formData);

    // Ejecutamos la petición POST a tu servidor Django
    await crearArea(payload);

    mostrarExito.value = true;
  } catch (error: any) {
    console.error("Error al crear el área:", error);

    if (error.response?.data?.errors) {
      // Mapeo del nuevo formato: { status: "error", errors: [{ campo, mensaje }] }
      error.response.data.errors.forEach((err: any) => {
        validationErrors.value[err.campo] = err.mensaje;
      });
      errorMsg.value = "Por favor, revise los campos marcados.";
    } else if (error.response?.data) {
      const data = error.response.data;
      errorMsg.value = data.error || "Ocurrió un error al validar los datos.";
    } else {
      errorMsg.value = "No se pudo establecer conexión con el servidor.";
    }
  } finally {
    cargando.value = false;
  }
}

// 3. Cancelación del flujo
function handleCancel() {
  router.push({ name: "areas" });
}

function irAlListado() {
  router.push({ name: "areas" });
}
</script>

<template>
  <div class="view-container">
    <header class="view-header">
      <h1>Crear Nueva Área</h1>
    </header>

    <DynamicForm
      :fields="areaFields"
      :loading="cargando"
      :error-msg="errorMsg"
      :validation-errors="validationErrors"
      :show-cancel="true"
      submit-label="Guardar Área"
      @submit="handleFormSubmit"
      @cancel="handleCancel"
    />

    <SuccessModal
      :show="mostrarExito"
      title="¡Área Guardada!"
      message="La nueva área ha sido registrada exitosamente en la organización."
      @confirm="irAlListado"
    />
  </div>
</template>

<style scoped>
.view-container {
  width: 95%;
  max-width: 600px;
  margin: 1rem auto;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

@media (min-width: 768px) {
  .view-container {
    margin: 2rem auto;
    padding: 2rem;
  }
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