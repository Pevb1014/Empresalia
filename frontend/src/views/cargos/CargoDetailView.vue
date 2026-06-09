<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { obtenerCargo, actualizarCargo, eliminarCargo } from "@/api/cargo.api.ts";
import { listarAreas } from "@/api/area.api.ts";
import { adaptCargoToForm, adaptFormToCargoPayload } from "@/adapters/cargos.adapter";
import DynamicForm, { type FormField } from "@/components/DynamicForm.vue";
import ActionModal from "@/components/ActionModal.vue";

const props = defineProps<{
  id: string;
}>();
const router = useRouter();

const cargo = ref<any>(null);
const cargoFormData = ref<any>(null);
const editando = ref(false);
const cargando = ref(true);
const procesando = ref(false);
const errorMsg = ref("");

const modal = ref({
  show: false,
  title: "",
  message: "",
  type: "confirm" as "confirm" | "info" | "error"
});

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

async function cargarDetalle() {
  try {
    cargando.value = true;
    const [resCargo, resAreas] = await Promise.all([
      obtenerCargo(props.id),
      listarAreas()
    ]);

    cargo.value = resCargo.data;
    cargoFormData.value = adaptCargoToForm(resCargo.data);

    const areaSelect = cargoFields.value.find(f => f.key === "area");
    if (areaSelect) {
      areaSelect.options = resAreas.data.results.map((area: any) => ({
        value: area.id,
        label: area.nombre,
      }));
    }
  } catch (error) {
    console.error(error);
    errorMsg.value = "No se pudo cargar el detalle del cargo.";
  } finally {
    cargando.value = false;
  }
}

onMounted(() => {
  cargarDetalle();
});

function iniciarEliminacion() {
  modal.value = {
    show: true,
    title: "Eliminar Cargo",
    message: `¿Estás seguro de que deseas eliminar el cargo "${cargo.value.nombre}"?`,
    type: "confirm"
  };
}

async function ejecutarEliminacion() {
  procesando.value = true;
  try {
    await eliminarCargo(props.id);
    modal.value = {
      show: true,
      title: "Cargo Eliminado",
      message: "El registro ha sido removido del sistema.",
      type: "info"
    };
  } catch (error) {
    modal.value = {
      show: true,
      title: "Acción Denegada",
      message: "No se puede eliminar el cargo porque tiene empleados activos asociados.",
      type: "error"
    };
  } finally {
    procesando.value = false;
  }
}

function cerrarModal() {
  const exito = modal.value.type === 'info';
  modal.value.show = false;
  if (exito) {
    router.push({ name: "cargos" });
  }
}

async function handleUpdateSubmit(formData: Record<string, any>) {
  procesando.value = true;
  errorMsg.value = "";

  try {
    const payload = adaptFormToCargoPayload(formData);
    const res = await actualizarCargo(props.id, payload);
    
    cargo.value = res.data;
    cargoFormData.value = adaptCargoToForm(res.data);
    editando.value = false;
  } catch (error: any) {
    console.error("Error al actualizar:", error);
    errorMsg.value = error.response?.data?.nombre?.[0] || "Error al actualizar el cargo.";
  } finally {
    procesando.value = false;
  }
}
</script>

<template>
  <div class="detail-container">
    <div v-if="cargando">Cargando detalles del cargo...</div>
    
    <div v-else-if="errorMsg && !editando" class="alerta-error">
      {{ errorMsg }}
    </div>

    <div v-else>
      <div v-if="!editando">
        <h1>Detalle del Cargo: {{ cargo.nombre }}</h1>
        <hr />
        
        <div class="info-group">
          <p><strong>Cargo:</strong> {{ cargo.nombre }}</p>
          <p><strong>Área:</strong> {{ cargo.area?.nombre || 'Sin área asignada' }}</p>
          <p><strong>Descripción:</strong> {{ cargo.descripcion || 'Sin descripción' }}</p>
        </div>

        <div class="acciones">
          <button @click="router.push({ name: 'cargos' })" :disabled="procesando" class="btn-secundario">
            Volver al listado
          </button>
          
          <button @click="iniciarEliminacion" :disabled="procesando" class="btn-peligro">
            {{ procesando ? "Eliminando..." : "Eliminar Cargo" }}
          </button>
          
          <button @click="editando = true" :disabled="procesando" class="btn-primario">
            Editar Cargo
          </button>
        </div>
      </div>

      <div v-else>
        <h1>Modificar Cargo</h1>
        <hr />
        <DynamicForm
          :fields="cargoFields"
          :initial-data="cargoFormData"
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

  <ActionModal
    :show="modal.show"
    :title="modal.title"
    :message="modal.message"
    :type="modal.type"
    :loading="procesando"
    @confirm="ejecutarEliminacion"
    @close="cerrarModal"
  />
</template>

<style scoped>
.detail-container { max-width: 600px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
hr { margin: 1rem 0 1.5rem 0; border: 0; border-top: 1px solid #eee; }
.info-group p { margin-bottom: 1rem; font-size: 1.1rem; }
.acciones { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; }
.btn-primario { background: #1976d2; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.btn-secundario { background: #e0e0e0; color: #333; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.btn-peligro { background: #d32f2f; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.alerta-error { background: #fbe9e7; color: #d32f2f; padding: 0.8rem; border-radius: 4px; }
button:disabled { opacity: 0.6; cursor: not-allowed; }

@media (max-width: 640px) {
  .detail-container { margin: 1rem; padding: 1.5rem; }
  .acciones { flex-direction: column; }
  .btn-primario, .btn-secundario, .btn-peligro { width: 100%; text-align: center; }
}
</style>