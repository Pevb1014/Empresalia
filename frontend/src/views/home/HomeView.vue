<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <main class="home-container">
    <!-- Hero Section -->
    <section class="hero">
      <h1>Empresalia</h1>
      <p class="subtitle">Gestión inteligente de capital humano y estructura organizacional.</p>
      <div class="actions">
        <RouterLink to="/empleados" class="btn-primary">Gestionar Personal</RouterLink>
        <RouterLink to="/areas" class="btn-secondary">Ver Estructura</RouterLink>
      </div>
    </section>

    <!-- Navigation Grid -->
    <section class="features">
      <RouterLink to="/areas" class="feature-card">
        <div class="icon">🏢</div>
        <h3>Gestión de Áreas</h3>
        <p>Configure los departamentos de la empresa. Defina la base de la estructura organizacional.</p>
      </RouterLink>

      <RouterLink to="/cargos" class="feature-card">
        <div class="icon">💼</div>
        <h3>Gestión de Cargos</h3>
        <p>Administre los niveles jerárquicos y puestos de trabajo vinculados a cada área corporativa.</p>
      </RouterLink>

      <RouterLink to="/empleados" class="feature-card">
        <div class="icon">👥</div>
        <h3>Control de Empleados</h3>
        <p>Registro completo de personal, gestión de estados, correos corporativos y asignaciones.</p>
      </RouterLink>

      <RouterLink to="/historial" class="feature-card">
        <div class="icon">🛡️</div>
        <h3>Auditoría y Control</h3>
        <p>Revise el historial de cambios detallado. Rastree quién, cuándo y qué se modificó en el sistema.</p>
      </RouterLink>
    </section>
  </main>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hero {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 3rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #4a5568;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn-primary { 
  background: #3498db; color: white; padding: 12px 24px; border-radius: 6px; 
  font-weight: bold; text-decoration: none; transition: background 0.2s;
}
.btn-primary:hover { background: #2980b9; }

.btn-secondary { 
  background: white; color: #3498db; border: 2px solid #3498db; padding: 10px 22px; 
  border-radius: 6px; font-weight: bold; text-decoration: none; transition: all 0.2s;
}
.btn-secondary:hover { background: #ebf5fb; }

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
  text-align: center;
  text-decoration: none;
  display: block;
  border: 1px solid #f0f0f0;
}

.feature-card:hover { 
  transform: translateY(-8px); 
  box-shadow: 0 8px 25px rgba(52, 152, 219, 0.15);
  border-color: #3498db;
}

.feature-card:hover { transform: translateY(-5px); }
.feature-card .icon { font-size: 2.5rem; margin-bottom: 15px; }
.feature-card h3 { color: #2c3e50; margin-bottom: 10px; }
.feature-card p { color: #5f6368; font-size: 0.95rem; line-height: 1.5; }

@media (max-width: 768px) {
  .hero h1 { font-size: 2rem; }
  .actions {
    flex-direction: column;
    padding: 0 20px;
  }
  .btn-primary, .btn-secondary { width: 100%; text-align: center; }
}
</style>