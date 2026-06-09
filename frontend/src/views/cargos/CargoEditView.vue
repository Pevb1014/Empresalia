<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { obtenerCargo, actualizarCargo } from "@/api/cargo.api.ts";
import { listarAreas } from "@/api/area.api.ts";
import { adaptCargoToForm, adaptFormToCargoPayload } from "@/adapters/cargos.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import SuccessModal from "@/components/SuccessModal.vue";

const route = useRoute();
const router = useRouter();
const cargoId = route.params.id as string;

const cargoFormData = ref<any>(null);
const cargando = ref(true);
const guardando = ref(false);
const mostrarExito = ref(false);
const errorMsg = ref("");
const validationErrors = ref<Record<string, string>>({});

const cargoFields = ref<FormField[]>([
  { key: "nombre", label: "Nombre del Cargo", type: "text", required: true },
  { key: "area", label: "Área de la Empresa", type: "select", required: true, options: [] },
  { 
    key: "descripcion", 
    label: "Descripción", 
    type: "textarea", 
    placeholder: "Escriba las funciones o responsabilidades...",
    required: false 
  },
]);

onMounted(async () => {
  try {
    // Carga paralela del cargo y las áreas del selector
    const [resCargo, resAreas] = await Promise.all([
      obtenerCargo(cargoId),
      listarAreas()
    ]);

    // Llenamos las opciones del select
    const areaSelect = cargoFields.value.find(f => f.key === "area");
    if (areaSelect) {
      areaSelect.options = resAreas.data.results.map((area: any) => ({
        value: area.id,
        label: area.nombre,
      }));
    }

    // Adaptamos el cargo para los inputs del formulario
    cargoFormData.value = adaptCargoToForm(resCargo.data);
  } catch (error) {
    console.error(error);
    errorMsg.value = "Error al recuperar los datos del cargo.";
  } finally {
    cargando.value = false;
  }
});

async function handleUpdateSubmit(formData: Record<string, any>) {
  guardando.value = true;
  errorMsg.value = "";
  validationErrors.value = {};

  try {
    const payload = adaptFormToCargoPayload(formData);
    await actualizarCargo(cargoId, payload);

    mostrarExito.value = true;
  } catch (error: any) {
    console.error(error);
    if (error.response?.data?.errors) {
      error.response.data.errors.forEach((err: any) => {
        validationErrors.value[err.campo] = err.mensaje;
      });
      errorMsg.value = "Error de validación.";
    } else {
      errorMsg.value = "No se pudieron guardar los cambios en el servidor.";
    }
  } finally {
    guardando.value = false;
  }
}

function handleCancel() {
  router.push({ name: "cargo-detail", params: { id: cargoId } });
}

function irAlDetalle() {
  router.push({ name: "cargo-detail", params: { id: cargoId } });
}
</script>

<template>
  <div class="view-container">
    <div v-if="cargando">Preparando formulario...</div>
    
    <div v-else>
      <h1>Modificar Cargo</h1>
      <hr />
      
      <DynamicForm
        :fields="cargoFields"
        :initial-data="cargoFormData"
        :loading="guardando"
        :error-msg="errorMsg"
        :validation-errors="validationErrors"
        :show-cancel="true"
        submit-label="Guardar Cambios"
        @submit="handleUpdateSubmit"
        @cancel="handleCancel"
      />

      <SuccessModal
        :show="mostrarExito"
        title="¡Cargo Actualizado!"
        message="Los cambios en el cargo se han guardado con éxito."
        @confirm="irAlDetalle"
      />
    </div>
  </div>
</template>

<style scoped>
.view-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}
.view-header { margin-bottom: 1.5rem; border-bottom: 1px solid #f0f0f0; padding-bottom: 0.5rem; }

@media (max-width: 640px) {
  .view-container {
    margin: 1rem;
    padding: 1.5rem;
  }
}
</style>