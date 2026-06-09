<script setup lang="ts">
import { ref, watch } from "vue";

// Definición de la estructura de cada campo (equivalente a tus 'columns')
export interface FormField {
  key: string;
  label: string;
  type: "text" | "textarea" | "number" | "select" | "date" | "email";
  placeholder?: string;
  required?: boolean;
  options?: { value: any; label: string }[];
}

const props = defineProps<{
  fields: FormField[];
  initialData?: Record<string, any>;
  loading?: boolean;
  errorMsg?: string;
  validationErrors?: Record<string, string>;
  showCancel?: boolean;
  submitLabel?: string;
}>();

const emit = defineEmits<{
  (e: "submit", formData: Record<string, any>): void;
  (e: "cancel"): void;
}>();

// Estado interno reactivo que almacena los valores del formulario
const formData = ref<Record<string, any>>({});

// Sincroniza datos iniciales cuando se edita o carga información asíncrona
watch(
  () => props.initialData,
  (newData) => {
    if (newData) {
      formData.value = { ...newData };
    }
  },
  { immediate: true, deep: true }
);

function handleSubmit() {
  emit("submit", { ...formData.value });
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="dynamic-form">
    
    <div v-if="errorMsg" class="form-error">
      {{ errorMsg }}
    </div>

    <div v-for="field in fields" :key="field.key" class="form-group">
      <label :for="field.key">
        {{ field.label }} <span v-if="field.required">*</span>
      </label>

      <textarea
        v-if="field.type === 'textarea'"
        :id="field.key"
        v-model="formData[field.key]"
        :placeholder="field.placeholder"
        :required="field.required"
        :class="{ 'input-invalid': validationErrors?.[field.key] }"
        :disabled="loading"
      ></textarea>

      <select
        v-else-if="field.type === 'select'"
        :id="field.key"
        v-model="formData[field.key]"
        :required="field.required"
        :class="{ 'input-invalid': validationErrors?.[field.key] }"
        :disabled="loading"
      >
        <option value="" disabled>{{ field.placeholder || 'Seleccione una opción' }}</option>
        <option 
          v-for="opt in field.options" 
          :key="opt.value" 
          :value="opt.value"
        >
          {{ opt.label }}
        </option>
      </select>

      <input
        v-else
        :id="field.key"
        v-model="formData[field.key]"
        :type="field.type"
        :placeholder="field.placeholder"
        :class="{ 'input-invalid': validationErrors?.[field.key] }"
        :required="field.required"
        :disabled="loading"
      />

      <span v-if="validationErrors?.[field.key]" class="field-error">
        {{ validationErrors[field.key] }}
      </span>
    </div>

    <div class="form-actions">
      <slot name="actions">
        <button 
          v-if="showCancel" 
          type="button" 
          @click="emit('cancel')" 
          :disabled="loading"
          class="btn-cancel"
        >
          Cancelar
        </button>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="btn-submit"
        >
          {{ loading ? "Procesando..." : submitLabel || "Guardar" }}
        </button>
      </slot>
    </div>

  </form>
</template>

<style scoped>
/* Estilos estructurales limpios */
.dynamic-form { display: flex; flex-direction: column; gap: 1.2rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
label { font-weight: 600; font-size: 0.95rem; }
input, textarea, select { padding: 0.75rem; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; transition: border-color 0.2s; }
input:focus, textarea:focus, select:focus { outline: none; border-color: var(--primary); }
.form-error { background: #fee2e2; color: var(--danger); padding: 1rem; border-radius: 8px; border-left: 4px solid var(--danger); font-weight: 500; }
.form-actions { display: flex; justify-content: flex-end; gap: 0.8rem; margin-top: 1rem; }
.btn-submit { background: var(--primary); color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
.btn-submit:hover { background: var(--primary-dark); }
.input-invalid { border-color: var(--danger) !important; background-color: #fef2f2; }
.field-error { color: var(--danger); font-size: 0.85rem; font-weight: 500; margin-top: 0.2rem; }
.btn-cancel { background: var(--secondary); color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: opacity 0.2s; }
.btn-cancel:hover { opacity: 0.9; }
button:disabled { opacity: 0.6; cursor: not-allowed; }

@media (max-width: 640px) {
  .dynamic-form { gap: 1rem; }
  .form-actions { flex-direction: column-reverse; }
  .btn-submit, .btn-cancel { width: 100%; text-align: center; }
  input, textarea, select { font-size: 16px; } /* Evita zoom automático en móviles */
}
</style>