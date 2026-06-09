<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
// Importamos eliminarArea junto con las demás funciones de la API
import { obtenerArea, actualizarArea, eliminarArea } from "@/api/area.api";
import { adaptAreaToForm, adaptFormToAreaPayload } from "@/adapters/areas.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";

const props = defineProps<{
  id: string;
}>();
const router = useRouter();

// Estados de la vista
const areaRaw = ref<any>(null);
const areaFormData = ref<any>(null);
const editando = ref(false);
const cargando = ref(true);
const procesando = ref(false); // Reutilizado para guardar o eliminar
const errorMsg = ref("");

const areaFields: FormField[] = [
  { key: "nombre", label: "Nombre del Área", type: "text", required: true },
  { key: "descripcion", label: "Descripción", type: "textarea" },
];

async function cargarDetalle() {
  try {
    cargando.value = true;
    const res = await obtenerArea(props.id);
    areaRaw.value = res.data;
    areaFormData.value = adaptAreaToForm(res.data);
  } catch (error) {
    console.error("Error al cargar el detalle:", error);
    errorMsg.value = "No se pudo cargar la información del área.";
  } finally {
    cargando.value = false;
  }
}

onMounted(() => {
  cargarDetalle();
});

async function handleUpdateSubmit(formData: Record<string, any>) {
  procesando.value = true;
  errorMsg.value = "";

  try {
    const payload = adaptFormToAreaPayload(formData);
    const res = await actualizarArea(props.id, payload);
    
    areaRaw.value = res.data;
    areaFormData.value = adaptAreaToForm(res.data);
    editando.value = false;
  } catch (error: any) {
    console.error("Error al actualizar:", error);
    if (error.response?.data) {
      errorMsg.value = error.response.data.nombre?.[0] || "Error al actualizar el área.";
    } else {
      errorMsg.value = "Error de comunicación con el servidor.";
    }
  } finally {
    procesando.value = false;
  }
}

// 🔹 Nueva función para manejar la eliminación desde el detalle
async function handleEliminar() {
  const confirmar = confirm(`¿Estás seguro de que deseas eliminar definitivamente el área "${areaRaw.value.nombre}"?`);
  
  if (!confirmar) return;

  procesando.value = true;
  errorMsg.value = "";

  try {
    await eliminarArea(props.id);
    // Redirección al listado tras borrar con éxito
    router.push({ name: "areas" });
  } catch (error) {
    console.error("Error al eliminar el área:", error);
    errorMsg.value = "No se pudo eliminar el área. Asegúrate de que no tenga cargos asociados en Django.";
    procesando.value = false;
  }
}
</script>

<template>
  <div class="detail-container">
    <div v-if="cargando">Cargando detalles...</div>
    
    <div v-else-if="errorMsg && !editando" class="alerta-error">
      {{ errorMsg }}
    </div>

    <div v-else>
      <div v-if="!editando">
        <h1>Detalle del Área: {{ areaRaw.nombre }}</h1>
        <hr />
        <div class="info-group">
          <p><strong>Nombre:</strong> {{ areaRaw.nombre }}</p>
          <p><strong>Descripción:</strong> {{ areaRaw.descripcion || 'Sin descripción' }}</p>
        </div>

        <div class="acciones">
          <button @click="router.push({ name: 'areas' })" :disabled="procesando" class="btn-secundario">
            Volver al listado
          </button>
          
          <button @click="handleEliminar" :disabled="procesando" class="btn-peligro">
            {{ procesando ? "Eliminando..." : "Eliminar Área" }}
          </button>
          
          <button @click="editando = true" :disabled="procesando" class="btn-primario">
            Editar Área
          </button>
        </div>
      </div>

      <div v-else>
        <h1>Modificar Área</h1>
        <hr />
        <DynamicForm
          :fields="areaFields"
          :initial-data="areaFormData"
          :loading="procesando"
          :error-msg="errorMsg"
          :show-cancel="true"
          submit-label="Guardar Cambios"
          @submit="handleUpdateSubmit"
          @cancel="editando = false"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-container { max-width: 600px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
hr { margin: 1rem 0 1.5rem 0; border: 0; border-top: 1px solid #eee; }
.info-group p { margin-bottom: 1rem; font-size: 1.1rem; }
.acciones { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; }
.btn-primario { background: #1976d2; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.btn-secundario { background: #e0e0e0; color: #333; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
/* Estilo para el botón de eliminar */
.btn-peligro { background: #d32f2f; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.alerta-error { background: #fbe9e7; color: #d32f2f; padding: 0.8rem; border-radius: 4px; margin-bottom: 1rem; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>