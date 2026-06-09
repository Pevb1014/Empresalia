<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { adaptHistorialToDetail } from "@/adapters/historial.adapter";

const props = defineProps<{ id: string }>();
const router = useRouter();

const registro = ref<any>(null);
const cargando = ref(true);
const errorMsg = ref("");

async function cargarDetalle() {
  try {
    cargando.value = true;
    const res = await api.get(`historial/${props.id}/`);
    registro.value = adaptHistorialToDetail(res.data);
  } catch (error) {
    errorMsg.value = "No se pudo cargar el detalle de la auditoría.";
  } finally {
    cargando.value = false;
  }
}

onMounted(cargarDetalle);
</script>

<template>
  <div class="view-card detail-view">
    <div v-if="cargando">Cargando detalle...</div>
    <div v-else-if="errorMsg" class="alerta-error">{{ errorMsg }}</div>
    <div v-else>
      <header class="view-header">
        <h1>Evento de Auditoría</h1>
      </header>

      <div class="info-grid">
        <div class="info-item">
          <p class="label">Empleado</p>
          <p class="value">{{ registro.empleado }}</p>
        </div>
        <div class="info-item">
          <p class="label">Fecha del Registro</p>
          <p class="value">{{ registro.fecha }}</p>
        </div>
        <div class="info-item">
          <p class="label">Operación</p>
          <span class="tag-operacion">{{ registro.tipo }}</span>
        </div>
        <div class="info-item">
          <p class="label">Campo Afectado</p>
          <p class="value"><code>{{ registro.campo }}</code></p>
        </div>
      </div>

      <div class="comparativa" v-if="registro.tipo === 'ACTUALIZACION'">
        <div class="valor-box">
          <label>Valor Anterior</label>
          <div class="valor original">{{ registro.valor_anterior || '(Vacío)' }}</div>
        </div>
        <div class="valor-box">
          <label>Valor Nuevo</label>
          <div class="valor nuevo">{{ registro.valor_nuevo }}</div>
        </div>
      </div>
      <div v-else class="comparativa">
        <p>Registro inicial creado con el valor: <strong>{{ registro.valor_nuevo }}</strong></p>
      </div>

      <div class="acciones">
        <button @click="router.push({ name: 'historial' })" class="btn-secundario">Volver al listado</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-header { margin-bottom: 1.5rem; border-bottom: 1px solid #f0f0f0; padding-bottom: 0.5rem; }
.subtitle { color: #666; font-size: 0.85rem; margin-top: 0.2rem; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }
.comparativa { display: flex; flex-wrap: wrap; gap: 2rem; background: #f9f9f9; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border: 1px solid #eee; }
.valor-box { flex: 1; }
.valor-box label { display: block; font-size: 0.8rem; text-transform: uppercase; color: #777; margin-bottom: 0.5rem; }
.valor { padding: 1rem; border-radius: 4px; font-family: monospace; }
.original { background: #fee2e2; color: #991b1b; text-decoration: line-through; }
.nuevo { background: #dcfce7; color: #166534; }
.tag-operacion { background: #e0e7ff; color: #3730a3; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; font-size: 0.9rem; }
.acciones { display: flex; justify-content: flex-end; }
.btn-secundario { background: #e0e0e0; color: #333; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; }
.alerta-error { background: #fbe9e7; color: #d32f2f; padding: 0.8rem; border-radius: 4px; margin-bottom: 1rem; }

@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; gap: 1rem; }
  .comparativa { flex-direction: column; gap: 1rem; }
  .acciones { justify-content: center; }
  .btn-secundario { width: 100%; }
}
</style>