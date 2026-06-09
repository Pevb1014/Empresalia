<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { obtenerEmpleado, actualizarEmpleado } from "@/api/empleado.api.ts";
import { listarCargos } from "@/api/cargo.api.ts";
import { adaptEmpleadoToForm, adaptFormToEmpleadoPayload } from "@/adapters/empleados.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import SuccessModal from "@/components/SuccessModal.vue";

const route = useRoute();
const router = useRouter();
const empleadoId = route.params.id as string;

const empleadoFormData = ref<any>(null);
const cargando = ref(true);
const guardando = ref(false);
const mostrarExito = ref(false);
const errorMsg = ref("");
const validationErrors = ref<Record<string, string>>({});

const empleadoFields = ref<FormField[]>([
  { key: "numero_documento", label: "Número de Documento", type: "text", required: true },
  { key: "nombre", label: "Nombre", type: "text", required: true },
  { key: "correo", label: "Correo Electrónico", type: "email", required: true },
  { key: "fecha_ingreso", label: "Fecha de Ingreso", type: "date", required: true },
  {
    key: "estado",
    label: "Estado Operativo",
    type: "select",
    required: true,
    options: [{ value: "ACTIVO", label: "Activo" }, { value: "INACTIVO", label: "Inactivo" }]
  },
  { key: "cargo", label: "Cargo Asignado", type: "select", required: true, options: [] },
]);

onMounted(async () => {
  try {
    const [resEmpleado, resCargos] = await Promise.all([
      obtenerEmpleado(empleadoId),
      listarCargos()
    ]);

    const cargoSelect = empleadoFields.value.find(f => f.key === "cargo");
    if (cargoSelect) {
      cargoSelect.options = resCargos.data.results.map((c: any) => ({
        value: c.id,
        label: c.nombre
      }));
    }

    empleadoFormData.value = adaptEmpleadoToForm(resEmpleado.data);
  } catch (error) {
    console.error(error);
    errorMsg.value = "No se pudieron cargar los datos del empleado.";
  } finally {
    cargando.value = false;
  }
});

async function handleUpdateSubmit(formData: Record<string, any>) {
  guardando.value = true;
  errorMsg.value = "";
  validationErrors.value = {};

  try {
    const payload = adaptFormToEmpleadoPayload(formData);
    await actualizarEmpleado(empleadoId, payload);
    mostrarExito.value = true;
  } catch (error: any) {
    console.error(error);
    if (error.response?.data?.errors) {
      error.response.data.errors.forEach((err: any) => {
        validationErrors.value[err.campo] = err.mensaje;
      });
      errorMsg.value = "Error de validación.";
    } else {
      errorMsg.value = "Error al intentar actualizar la ficha.";
    }
  } finally {
    guardando.value = false;
  }
}

function irAlDetalle() {
  router.push({ name: "empleado-detail", params: { id: empleadoId } });
}
</script>

<template>
  <div class="edit-container">
    <div v-if="cargando">Preparando datos del empleado...</div>
    
    <div v-else>
      <h1>Modificar Ficha de Empleado</h1>
      <hr />
      
      <DynamicForm
        :fields="empleadoFields"
        :initial-data="empleadoFormData"
        :loading="guardando"
        :error-msg="errorMsg"
        :validation-errors="validationErrors"
        :show-cancel="true"
        submit-label="Actualizar"
        @submit="handleUpdateSubmit"
        @cancel="router.push({ name: 'empleado-detail', params: { id: empleadoId } })"
      />

      <SuccessModal
        :show="mostrarExito"
        title="¡Datos Actualizados!"
        message="La información del empleado se ha actualizado correctamente en el sistema."
        @confirm="irAlDetalle"
      />
    </div>
  </div>
</template>

<style scoped>
.edit-container { max-width: 600px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
hr { margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eee; }

@media (max-width: 640px) {
  .edit-container {
    margin: 1rem;
    padding: 1.5rem;
    max-width: none;
  }
}
</style>