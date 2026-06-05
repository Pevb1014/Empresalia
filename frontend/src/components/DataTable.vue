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
  <table>
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key">
          {{ col.label }}
        </th>
        <th>Acciones</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="item in data" :key="item.id">
        <td v-for="col in columns" :key="col.key">
          {{ getValue(item, col.key) }}
        </td>

        <td>
          <button @click="emit('detail', item)">
            Ver detalle
          </button>

          <button v-if="showEdit" @click="emit('edit', item)">
            Editar
          </button>

          <button v-if="showDelete" @click="emit('delete', item)">
            Eliminar
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>