<script setup lang="ts">
/**
 * Componente Modal Reutilizable para Acciones y Mensajes
 */
defineProps<{
  show: boolean;
  title: string;
  message: string;
  type: 'confirm' | 'info' | 'error';
  loading?: boolean;
}>();

const emit = defineEmits(['confirm', 'close']);
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="show" class="modal-overlay" @click.self="emit('close')">
        <div class="modal-content" role="dialog">
          <h3 :class="['modal-title', type]">{{ title }}</h3>
          <p class="modal-message">{{ message }}</p>
          
          <div class="modal-actions">
            <!-- Botones para flujo de confirmación -->
            <template v-if="type === 'confirm'">
              <button @click="emit('close')" :disabled="loading" class="btn-secundario">
                Cancelar
              </button>
              <button @click="emit('confirm')" :disabled="loading" class="btn-peligro">
                {{ loading ? 'Eliminando...' : 'Eliminar definitivamente' }}
              </button>
            </template>
            
            <!-- Botón para flujo de información (Éxito o Error) -->
            <template v-else>
              <button @click="emit('close')" class="btn-primario">
                Aceptar
              </button>
            </template>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5); display: flex; align-items: center;
  justify-content: center; z-index: 3000; backdrop-filter: blur(2px);
}
.modal-content {
  background: white; padding: 2rem; border-radius: 12px; width: 90%;
  max-width: 450px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}
.modal-title { margin-top: 0; font-size: 1.4rem; }
.modal-title.confirm { color: #1976d2; }
.modal-title.error { color: #d32f2f; }
.modal-title.info { color: #2e7d32; }
.modal-message { font-size: 1.1rem; color: #555; line-height: 1.5; margin: 1rem 0; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; }

.btn-primario { background: #1976d2; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.btn-secundario { background: #e0e0e0; color: #333; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.btn-peligro { background: #d32f2f; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
button:disabled { opacity: 0.6; cursor: not-allowed; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 480px) {
  .modal-content { padding: 1.5rem; width: 95%; }
  .modal-actions { flex-direction: column-reverse; gap: 0.75rem; }
  .btn-primario, .btn-secundario, .btn-peligro { width: 100%; padding: 0.8rem; }
}
</style>