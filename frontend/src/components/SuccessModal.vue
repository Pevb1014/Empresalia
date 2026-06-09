<script setup lang="ts">
/**
 * Componente de retroalimentación visual para operaciones exitosas.
 * Utiliza un diseño minimalista coherente con la identidad de Empresalia.
 */
defineProps<{
  show: boolean;
  title: string;
  message: string;
}>();

const emit = defineEmits<{
  (e: "confirm"): void;
}>();
</script>

<template>
  <Transition name="modal">
    <div v-if="show" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <div class="success-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          </div>

          <div class="modal-body">
            <h3>{{ title }}</h3>
            <p>{{ message }}</p>
          </div>

          <div class="modal-footer">
            <button class="modal-default-button" @click="emit('confirm')">
              Continuar
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-mask { position: fixed; z-index: 9998; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: table; transition: opacity 0.3s ease; }
.modal-wrapper { display: table-cell; vertical-align: middle; }
.modal-container { width: 350px; margin: 0px auto; padding: 2rem; background-color: #ffffff; border-radius: 12px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); text-align: center; }
.success-icon { background: #e6f7ed; color: #28a745; width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; }
.modal-body h3 { margin-top: 0; color: #1a1a1a; font-size: 1.25rem; margin-bottom: 0.5rem; }
.modal-body p { color: #666; margin-bottom: 1.5rem; line-height: 1.5; }
.modal-default-button { background: #1a1a1a; color: white; border: none; padding: 0.75rem 2rem; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; width: 100%; font-size: 1rem; }
.modal-default-button:hover { background: #333; }

/* Animación de entrada/salida */
.modal-enter-from { opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-enter-from .modal-container,
.modal-leave-to .modal-container { transform: scale(0.9); }

@media (max-width: 480px) {
  .modal-container { width: 90%; padding: 1.5rem; }
}
</style>