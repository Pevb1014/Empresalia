<script setup lang="ts">
defineProps<{
  data: any[]
  columns: { key: string; label: string }[]
  showEdit?: boolean   // 🔹 Control independiente para Editar
  showDelete?: boolean // 🔹 Control independiente para Eliminar
}>()

const emit = defineEmits<{
  (e: "detail", item: any): void
  (e: "edit", item: any): void
  (e: "delete", item: any): void
}>()

function getValue(obj: any, key: string) {
  return key.split(".").reduce((acc, k) => acc?.[k], obj)
}
</script>

<template>
  <div class="table-container">
    <table class="custom-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key">
            {{ col.label }}
          </th>
          <th class="actions-header">Acciones</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td v-for="col in columns" :key="col.key" class="border-cell">
            {{ getValue(item, col.key) }}
          </td>

          <td class="actions-cell">
            <button class="btn btn-detail" @click="emit('detail', item)" title="Ver detalle">
              👁️ Ver
            </button>

            <button v-if="showEdit" class="btn btn-edit" @click="emit('edit', item)" title="Editar">
              Editar
            </button>

            <button v-if="showDelete" class="btn btn-delete" @click="emit('delete', item)" title="Eliminar">
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.95rem;
}

.custom-table thead tr {
  background-color: #f8f9fa;
  color: #374151;
}

.custom-table th,
.custom-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

.custom-table tbody tr {
  transition: background-color 0.2s ease;
}

.custom-table tbody tr:nth-child(even) {
  background-color: #f9fafb; /* 🔹 Zebra striping */
}

.custom-table tbody tr:hover {
  background-color: #f3f4f6;
}

.actions-header {
  text-align: center;
}

.actions-cell {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.btn {
  padding: 6px 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn:hover {
  opacity: 0.8;
}

.btn-detail { background-color: var(--primary); color: white; }
.btn-edit { background-color: var(--warning); color: white; }
.btn-delete { background-color: var(--danger); color: white; }

/* Estilo para cuando no hay datos */
.custom-table tbody tr:last-of-type {
  border-bottom: none;
}

@media (max-width: 768px) {
  .actions-cell {
    flex-direction: column;
    align-items: stretch;
  }
  .btn {
    text-align: center;
    width: 100%;
    padding: 10px;
  }
}
</style>