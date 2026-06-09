<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <RouterLink to="/" class="nav-brand">Empresalia</RouterLink>
      <div class="nav-links">
        <RouterLink to="/areas" class="nav-item">
          Áreas
        </RouterLink>
        <RouterLink to="/cargos" class="nav-item">
          Cargos
        </RouterLink>
        <RouterLink to="/empleados" class="nav-item">
          Empleados
        </RouterLink>
        <RouterLink to="/historial" class="nav-item">
          Historial
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  padding: 0 1.5rem;
  height: 64px;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 0.25rem;
}

.nav-item {
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: #f3f4f6;
  color: var(--text-main);
}

.router-link-active {
  color: var(--primary);
  background-color: #f1f5f9;
}

@media (max-width: 768px) {
  .navbar { height: auto; padding: 1rem; }
  .nav-container { flex-direction: column; gap: 1rem; }
  .nav-links { 
    width: 100%;
    overflow-x: auto;
    padding: 0.5rem 0;
    justify-content: center;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .nav-links::-webkit-scrollbar { display: none; }
  .nav-item { white-space: nowrap; font-size: 0.9rem; padding: 0.4rem 0.75rem; }
}
</style>