<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  totalItems: number;
  pageSize: number;
  currentPage: number;
}>();

const emit = defineEmits(["update:currentPage"]);

const totalPages = computed(() => Math.ceil(props.totalItems / props.pageSize) || 1);

function changePage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    emit("update:currentPage", page);
  }
}
</script>

<template>
  <div class="pagination-container" v-if="totalPages > 1">
    <button 
      :disabled="currentPage === 1" 
      @click="changePage(currentPage - 1)"
      class="btn-page"
    >
      Anterior
    </button>

    <span class="page-info">
      Página {{ currentPage }} de {{ totalPages }}
    </span>

    <button 
      :disabled="currentPage === totalPages" 
      @click="changePage(currentPage + 1)"
      class="btn-page"
    >
      Siguiente
    </button>
  </div>
</template>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
}

.page-info {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.btn-page {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-page:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.btn-page:not(:disabled):hover {
  background: #f5f5f5;
}

@media (max-width: 480px) {
  .pagination-container { flex-wrap: wrap; gap: 0.5rem; }
  .page-info { order: -1; width: 100%; text-align: center; margin-bottom: 0.5rem; }
  .btn-page { flex: 1; padding: 0.6rem; }
}
</style>