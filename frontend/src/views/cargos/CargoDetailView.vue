<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { obtenerCargo, eliminarCargo } from "@/api/cargoApi";

const route = useRoute();
const router = useRouter();
const cargoId = route.params.id as string;

const cargo = ref<any>(null);
const cargando = ref(true);
const eliminando = ref(false);
const errorMsg = ref("");

onMounted(async () => {
  try {
    const res = await obtenerCargo(cargoId);
    cargo.value = res.data;
  } catch (error) {
    console.error(error);
    errorMsg.value = "No se pudo cargar el detalle del cargo.";
  } finally {
    cargando.value = false;
  }
});

async function handleEliminar() {
  const confirmar = confirm(`¿Deseas eliminar definitivamente el cargo "${cargo.value.nombre}"?`);
  if (!confirmar) return;

  eliminando.value = true;
  try {
    await eliminarCargo(cargoId);
    router.push({ name: "cargos" });
  } catch (error) {
    console.error(error);
    errorMsg.value = "No se pudo eliminar el cargo. Verifica dependencias en el servidor.";
    eliminando.value = false;
  }
}
</script>

<template>
  <div class="detail-container">
    <div v-if="cargando">Cargando detalles del cargo...</div>
    
    <div v-else-if="errorMsg" class="alerta-error">
      {{ errorMsg }}
    </div>

    <div v-else>
      <h1>Detalle del Cargo</h1>
      <hr />
      
      <div class="info-group">
        <p><strong>Cargo:</strong> {{ cargo.nombre }}</p>
        <p><strong>Área:</strong> {{ cargo.area?.nombre || 'Sin área asignada' }}</p>
      </div>

      <div class="acciones">
        <button @click="router.push({ name: 'cargos' })" :disabled="eliminando" class="btn-secundario">
          Volver al listado
        </button>
        
        <button @click="handleEliminar" :disabled="eliminando" class="btn-peligro">
          {{ eliminando ? "Eliminando..." : "Eliminar Cargo" }}
        </button>
        
        <button @click="router.push({ name: 'cargo-edit', params: { id: cargoId } })" :disabled="eliminando" class="btn-primario">
          Editar Cargo
        </button>
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
.btn-peligro { background: #d32f2f; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.alerta-error { background: #fbe9e7; color: #d32f2f; padding: 0.8rem; border-radius: 4px; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>