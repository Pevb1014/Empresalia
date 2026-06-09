<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { obtenerEmpleado, actualizarEmpleado, eliminarEmpleado } from "@/api/empleado.api.ts";
import { listarCargos } from "@/api/cargo.api.ts";
import { adaptEmpleadoToForm, adaptFormToEmpleadoPayload } from "@/adapters/empleados.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";

const props = defineProps<{ id: string }>();
const router = useRouter();

const empleado = ref<any>(null);
const empleadoFormData = ref<any>(null);
const editando = ref(false);
const cargando = ref(true);
const procesando = ref(false);
const errorMsg = ref("");

const empleadoFields = ref<FormField[]>([
  { key: "nombre", label: "Nombre", type: "text", required: true },
  { key: "numero_documento", label: "Documento", type: "text", required: true },
  { key: "correo", label: "Correo Electrónico", type: "email", required: true },
  { key: "fecha_ingreso", label: "Fecha de Ingreso", type: "date", required: true },
  { key: "cargo", label: "Cargo", type: "select", required: true, options: [] },
  { key: "estado", label: "Estado", type: "select", required: true, options: [
    { value: "ACTIVO", label: "Activo" },
    { value: "INACTIVO", label: "Inactivo" }
  ]},
]);

async function cargarDatos() {
  try {
    cargando.value = true;
    const [resEmp, resCargos] = await Promise.all([
      obtenerEmpleado(props.id),
      listarCargos()
    ]);

    empleado.value = resEmp.data;
    empleadoFormData.value = adaptEmpleadoToForm(resEmp.data);

    const cargoSelect = empleadoFields.value.find(f => f.key === "cargo");
    if (cargoSelect) {
      cargoSelect.options = resCargos.data.results.map((c: any) => ({
        value: c.id,
        label: c.nombre
      }));
    }
  } catch (error) {
    errorMsg.value = "No se pudieron cargar los datos del empleado.";
  } finally {
    cargando.value = false;
  }
}

onMounted(cargarDatos);

async function handleEliminar() {
  if (!confirm(`¿Eliminar a ${empleado.value.nombre}?`)) return;
  procesando.value = true;
  try {
    await eliminarEmpleado(props.id);
    router.push({ name: "empleados" });
  } catch (error) {
    errorMsg.value = "Error al intentar eliminar el registro.";
    procesando.value = false;
  }
}

async function handleUpdateSubmit(formData: Record<string, any>) {
  procesando.value = true;
  errorMsg.value = "";
  try {
    const payload = adaptFormToEmpleadoPayload(formData);
    const res = await actualizarEmpleado(props.id, payload);
    empleado.value = res.data;
    empleadoFormData.value = adaptEmpleadoToForm(res.data);
    editando.value = false;
  } catch (error: any) {
    errorMsg.value = error.response?.data?.nombre?.[0] || "Error al actualizar.";
  } finally {
    procesando.value = false;
  }
}
</script>

<template>
  <div class="view-container">
    <div v-if="cargando">Cargando...</div>
    <div v-else-if="errorMsg && !editando" class="alerta-error">{{ errorMsg }}</div>
    <div v-else>
      <div v-if="!editando">
        <header class="view-header">
          <h1>Ficha de Empleado: {{ empleado.nombre }}</h1>
        </header>
        
        <div class="info-grid">
          <p><strong>Documento:</strong> {{ empleado.numero_documento }}</p>
          <p><strong>Correo:</strong> {{ empleado.correo }}</p>
          <p><strong>Cargo:</strong> {{ empleado.cargo?.nombre }}</p>
          <p><strong>Área:</strong> {{ empleado.area?.nombre }}</p>
          <p><strong>Ingreso:</strong> {{ empleado.fecha_ingreso }}</p>
          <p><strong>Estado:</strong> 
            <span :class="empleado.estado === 'ACTIVO' ? 'tag-activo' : 'tag-inactivo'">
              {{ empleado.estado }}
            </span>
          </p>
        </div>

        <div class="acciones">
          <button @click="router.push({ name: 'empleados' })" class="btn-secundario">Volver</button>
          <button @click="handleEliminar" class="btn-peligro">Eliminar</button>
          <button @click="editando = true" class="btn-primario">Editar Ficha</button>
        </div>
      </div>

      <div v-else>
        <header class="view-header">
          <h1>Modificar Empleado</h1>
        </header>
        <DynamicForm
          :fields="empleadoFields"
          :initial-data="empleadoFormData"
          :loading="procesando"
          :error-msg="errorMsg"
          :show-cancel="true"
          @submit="handleUpdateSubmit"
          @cancel="editando = false"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-container { max-width: 700px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.view-header { margin-bottom: 1.5rem; border-bottom: 1px solid #f0f0f0; padding-bottom: 0.5rem; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }
.info-grid p { margin: 0; font-size: 1rem; }
.acciones { display: flex; justify-content: flex-end; gap: 1rem; }
.tag-activo { color: #2e7d32; font-weight: bold; }
.tag-inactivo { color: #d32f2f; font-weight: bold; }
.btn-primario { background: #1976d2; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; }
.btn-secundario { background: #e0e0e0; color: #333; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; }
.btn-peligro { background: #d32f2f; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; }
.alerta-error { background: #fbe9e7; color: #d32f2f; padding: 0.8rem; border-radius: 4px; margin-bottom: 1rem; }
</style>