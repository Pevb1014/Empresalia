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
        :disabled="loading"
      ></textarea>

      <select
        v-else-if="field.type === 'select'"
        :id="field.key"
        v-model="formData[field.key]"
        :required="field.required"
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
        :required="field.required"
        :disabled="loading"
      />
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
input, textarea, select { padding: 0.6rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
.form-error { background: #fbe9e7; color: #d32f2f; padding: 0.8rem; border-radius: 4px; border-left: 4px solid #d32f2f; }
.form-actions { display: flex; justify-content: flex-end; gap: 0.8rem; margin-top: 1rem; }
.btn-submit { background: #1976d2; color: white; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; }
.btn-cancel { background: #e0e0e0; color: #333; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>