# Empresalia - Frontend Portal

Este es el portal administrativo de **Empresalia**, una interfaz moderna e intuitiva construida para la gestión de la estructura organizacional, administración de personal y consulta de auditoría.

## 🚀 Tecnologías Principales

- **Vue 3**: Framework progresivo (utilizando Composition API).
- **Vite**: Herramienta de construcción ultra rápida.
- **TypeScript**: Tipado estático para garantizar la integridad de los datos consumidos de la API.
- **Vue Router**: Gestión de navegación entre módulos.

## 📁 Estructura de Datos (Interfaces)

El proyecto utiliza una arquitectura fuertemente tipada en `src/interfaces/` que espeja los modelos del backend para facilitar el mantenimiento:
- **Áreas y Cargos**: Gestión jerárquica de la empresa.
- **Empleados**: Ficha completa del personal con estados operativos.
- **Historial**: Seguimiento detallado de cambios (Auditoría) con soporte para filtros avanzados.

## 🛠️ Configuración del Entorno

### Configuración Recomendada del IDE
Use VS Code con la extensión oficial Vue - Volar (y deshabilite Vetur).

### Conexión con la API
Cree un archivo `.env` en la raíz basado en `.env.example`:
```env
VITE_API_URL=http://localhost:8000/api
```

### Instalación de Dependencias

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
