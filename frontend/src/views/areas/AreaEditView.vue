<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { obtenerArea, actualizarArea } from "@/api/area.api";
import { adaptAreaToForm, adaptFormToAreaPayload } from "@/adapters/areas.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import SuccessModal from "@/components/SuccessModal.vue";

const props = defineProps<{
  id: string;
}>();

const router = useRouter();
const cargando = ref(true);
const guardando = ref(false);
const mostrarExito = ref(false);
const areaFormData = ref<any>(null);
const errorMsg = ref("");
const validationErrors = ref<Record<string, string>>({});

const areaFields: FormField[] = [
  { key: "nombre", label: "Nombre del Área", type: "text", required: true },
  { key: "descripcion", label: "Descripción", type: "textarea" },
];

async function cargarDatos() {
  try {
    const res = await obtenerArea(props.id);
    areaFormData.value = adaptAreaToForm(res.data);
  } catch (error) {
    errorMsg.value = "No se pudo cargar la información del área.";
  } finally {
    cargando.value = false;
  }
}

onMounted(cargarDatos);

async function handleUpdate(formData: Record<string, any>) {
  guardando.value = true;
  errorMsg.value = "";
  validationErrors.value = {};

  try {
    const payload = adaptFormToAreaPayload(formData);
    await actualizarArea(props.id, payload);
    mostrarExito.value = true;
  } catch (error: any) {
    console.error("Error al actualizar:", error);
    if (error.response?.data?.errors) {
      error.response.data.errors.forEach((err: any) => {
        validationErrors.value[err.campo] = err.mensaje;
      });
      errorMsg.value = "Error de validación.";
    } else {
      errorMsg.value = "Error al actualizar el área.";
    }
  } finally {
    guardando.value = false;
  }
}

function irAlListado() {
  router.push({ name: "areas" });
}
</script>

<template>
  <div class="view-container">
    <h1>Editar Área</h1>
    <div v-if="cargando">Cargando...</div>
    <DynamicForm
      v-else
      :fields="areaFields"
      :initial-data="areaFormData"
      :loading="guardando"
      :error-msg="errorMsg"
      :validation-errors="validationErrors"
      :show-cancel="true"
      @submit="handleUpdate"
      @cancel="router.push({ name: 'areas' })"
    />

    <SuccessModal
      :show="mostrarExito"
      title="¡Área Actualizada!"
      message="Los cambios en el área han sido guardados correctamente."
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
  background: #fff;
  border-radius: 8px;
}

@media (min-width: 768px) {
  .view-container {
    margin: 2rem auto;
    padding: 2rem;
  }
}
</style>