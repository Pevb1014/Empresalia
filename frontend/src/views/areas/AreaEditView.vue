<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { obtenerArea, actualizarArea } from "@/api/area.api";
import { adaptAreaToForm, adaptFormToAreaPayload } from "@/adapters/areas.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";

const props = defineProps<{
  id: string;
}>();

const router = useRouter();
const cargando = ref(true);
const guardando = ref(false);
const areaFormData = ref<any>(null);
const errorMsg = ref("");

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
  try {
    const payload = adaptFormToAreaPayload(formData);
    await actualizarArea(props.id, payload);
    router.push({ name: "areas" });
  } catch (error: any) {
    errorMsg.value = "Error al actualizar el área.";
  } finally {
    guardando.value = false;
  }
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
      :show-cancel="true"
      @submit="handleUpdate"
      @cancel="router.push({ name: 'areas' })"
    />
  </div>
</template>

<style scoped>
.view-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
}
</style>