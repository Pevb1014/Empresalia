<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { obtenerEmpleado, actualizarEmpleado } from "@/api/empleadoApi";
import { listarCargos } from "@/api/cargoApi";
import { adaptEmpleadoToForm, adaptFormToEmpleadoPayload } from "@/adapters/empleados.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";

const route = useRoute();
const router = useRouter();
const empleadoId = route.params.id as string;

const empleadoFormData = ref<any>(null);
const cargando = ref(true);
const guardando = ref(false);
const errorMsg = ref("");

const empleadoFields = ref<FormField[]>([
  { key: "nombre", label: "Nombre", type: "text", required: true },
  { key: "apellido", label: "Apellido", type: "text", required: true },
  { key: "email", label: "Correo Electrónico", type: "email", required: true },
  { key: "cargo", label: "Cargo Asignado", type: "select", required: true, options: [] }
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

  try {
    const payload = adaptFormToEmpleadoPayload(formData);
    await actualizarEmpleado(empleadoId, payload);
    router.push({ name: "empleado-detail", params: { id: empleadoId } });
  } catch (error: any) {
    console.error(error);
    errorMsg.value = "Error al intentar actualizar la ficha.";
  } finally {
    guardando.value = false;
  }
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
        :show-cancel="true"
        submit-label="Actualizar"
        @submit="handleUpdateSubmit"
        @cancel="router.push({ name: 'empleado-detail', params: { id: empleadoId } })"
      />
    </div>
  </div>
</template>

<style scoped>
.edit-container { max-width: 600px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
hr { margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eee; }
</style>