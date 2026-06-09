<script setup lang="ts">
import AppNavbar from "@/components/AppNavbar.vue";
</script>

<template>
  <AppNavbar />

  <main>
    <RouterView />
  </main>
</template>

<style>
/* Sistema de Diseño Global - Moderno y Congruente */
:root {
  --primary: #1976d2;
  --primary-dark: #1565c0;
  --secondary: #64748b;
  --success: #10b981;
  --danger: #ef4444;
  --warning: #f59e0b;
  --bg-app: #f8fafc;
  --bg-card: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --border: #e2e8f0;
  --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --radius: 12px;
}

body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg-app);
  color: var(--text-main);
  line-height: 1.5;
}

main {
  padding: 2rem 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Clases comunes para todas las vistas */
.view-card {
  background: var(--bg-card);
  padding: 2rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: 2rem;
}

h1 { margin-top: 0; color: var(--text-main); font-weight: 700; }

@media (max-width: 640px) {
  main { padding: 1rem; }
  .view-card { padding: 1.25rem; }
  h1 { font-size: 1.8rem; }
}
</style>