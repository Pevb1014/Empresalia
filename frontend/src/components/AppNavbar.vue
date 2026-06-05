<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <nav class="navbar">
    <RouterLink to="/empleados">Empleados</RouterLink>

    <RouterLink to="/areas">Áreas</RouterLink>

    <RouterLink to="/cargos">Cargos</RouterLink>

    <RouterLink to="/historial">Historial</RouterLink>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

a {
  text-decoration: none;
  color: #333;
  font-weight: 600;
}

.router-link-active {
  color: #1976d2;
}
</style>