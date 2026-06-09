# Empresalia - Sistema de Gestión Organizacional

Empresalia es una plataforma integral diseñada para la gestión de personal, administración de la estructura organizacional (Áreas y Cargos) y auditoría detallada de cambios.

Este repositorio contiene tanto el núcleo de servicios (Backend) como el portal administrativo (Frontend).

---

## 🛠️ Tecnologías Principales

### Backend (API REST)
- **Python 3.10+**
- **Django 4.2+** & **Django Rest Framework (DRF)**
- **Django Filters**: Sistema de filtrado avanzado.
- **SQLite/PostgreSQL**: (Según configuración de base de datos).

### Frontend (Portal Web)
- **Vue 3**: Utilizando Composition API.
- **Vite**: Herramienta de construcción ultra rápida.
- **TypeScript**: Tipado estático para garantizar la integridad de los datos.
- **Vue Router**: Gestión de navegación.

---

## 🏗️ Arquitectura y Características

El proyecto sigue una filosofía de **separación de responsabilidades** y **tipado fuerte**:

1.  **Auditoría de Cambios (Rastro de Vida):** Característica crítica que registra automáticamente cada creación o actualización de empleados, almacenando el valor anterior, el valor nuevo y el campo modificado.
2.  **Validación y Normalización:** El backend normaliza automáticamente los nombres (capitalización) y valida la integridad (ej. no eliminar cargos con empleados activos).
3.  **Adaptadores y DTOs:** El frontend utiliza una capa de interfaces y adaptadores para transformar las respuestas de la API en modelos de datos listos para formularios dinámicos y tablas.
4.  **Paginación Estándar:** Resultados consistentes de 10 a 100 elementos por página.

---

## 🚀 Configuración del Entorno Local

### 1. Requisitos Previos
- Python 3.10 o superior.
- Node.js (Versión LTS recomendada).

### 2. Preparar el Backend
Desde la carpeta `/backend`:

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor (Por defecto en http://localhost:8000)
python manage.py runserver
```

### 3. Preparar el Frontend
Desde la carpeta `/frontend`:

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno (Basado en .env.example)
# VITE_API_URL=http://localhost:8000/api

# Iniciar servidor de desarrollo
npm run dev
```

---

## 🔍 Estructura de la API

| Recurso | Endpoint | Operaciones |
| :--- | :--- | :--- |
| **Empleados** | `/api/empleados/` | Listado, Detalle, Creación, Edición, Borrado |
| **Cargos** | `/api/cargos/` | Gestión de roles jerárquicos |
| **Áreas** | `/api/areas/` | Gestión de departamentos |
| **Auditoría** | `/api/historial/` | Consulta de historial de cambios (Solo lectura) |

---

## 📁 Estructura del Proyecto

```text
Empresalia/
├── backend/              # Lógica de negocio y API Django
│   ├── empleados/        # App principal (Models, Views, Serializers, Services)
│   └── core/             # Configuración del proyecto
├── frontend/             # Interfaz de usuario Vue.js
│   ├── src/
│   │   ├── adapters/     # Transformación de datos API -> UI
│   │   ├── interfaces/   # Contratos de TypeScript
│   │   └── views/        # Componentes de página
└── README.md             # Este archivo
```

---

## 📝 Notas de Desarrollo

- **Seguridad:** El sistema implementa `ProtectedError` para evitar la pérdida de integridad referencial.
- **Optimización:** Se hace uso extensivo de `select_related` y `prefetch_related` en el backend para minimizar las consultas a la base de datos (problema N+1).
