# Empresalia - Backend API

Este es el núcleo de servicios de la plataforma Empresalia, encargado de la gestión de personal, estructura organizacional y auditoría de cambios.

## 🚀 Tecnologías Principales

- **Python 3.10+**
- **Django 4.2+**: Framework web principal.
- **Django Rest Framework (DRF)**: Para la construcción de la API RESTful.
- **Django Filters**: Sistema de filtrado avanzado para endpoints.

## 🏗️ Arquitectura del Proyecto

El backend sigue un patrón de diseño basado en capas para asegurar el mantenimiento y la escalabilidad:

1. **Models (`/models`)**: Definición de la base de datos (Áreas, Cargos, Empleados, Historial de cambios). 
Incluyen validaciones de integridad y normalización de texto.
2. **Serializers (`/serializers`)**: Manejan la transformación de datos y validaciones de negocio. Utilizamos una estrategia de **división de responsabilidades**:
   - `ListSerializer`: Para respuestas ligeras en listados.
   - `DetailSerializer`: Para respuestas completas con relaciones anidadas.
   - `WriteSerializer`: Para procesos de creación y actualización con validaciones estrictas.
3. **Views (`/views`)**: Implementadas mediante `ModelViewSets` para agrupar la lógica de los endpoints (GET, POST, PUT, DELETE).
4. **Services (`/services`)**: Contienen la lógica de negocio que no pertenece estrictamente a un modelo o vista, como el sistema de auditoría.
5. **Pagination (`/pagination`)**: Esquema estándar de resultados (10 elementos por defecto, máximo 100).

## 🛡️ Sistema de Auditoría

Una característica crítica del sistema es el **Historial de Cambios**. Cada vez que se crea o actualiza un empleado, el sistema registra:
- El campo que cambió.
- El valor anterior y el valor nuevo.
- La fecha y el tipo de operación.

Esta lógica reside en `empleados/services/empleado_service.py` para mantener los modelos limpios y facilitar las pruebas unitarias.

## ⚡ Optimización de Consultas

Para garantizar un alto rendimiento, los ViewSets implementan técnicas de carga anticipada:
- `select_related`: Utilizado para relaciones `ForeignKey` simples (ej. Cargo -> Área).
- `prefetch_related`: Utilizado para relaciones inversas o de muchos a muchos (ej. Cargo -> Empleados).

## 🛠️ Configuración Local

1. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

4. **Iniciar servidor:**
   ```bash
   python manage.py runserver
   ```

## 🔍 Endpoints Principales

| Recurso | Endpoint | Métodos |
| :--- | :--- | :--- |
| **Empleados** | `/api/empleados/` | GET, POST, PUT, DELETE |
| **Cargos** | `/api/cargos/` | GET, POST, PUT, DELETE |
| **Áreas** | `/api/areas/` | GET, POST, PUT, DELETE |
| **Auditoría** | `/api/historial/` | GET (Solo lectura) |

## 📝 Notas de Desarrollo

- **Normalización:** Los nombres se normalizan automáticamente (Capitalización, eliminación de espacios extra) en el método `save()` de los modelos.
- **Seguridad:** No se permite eliminar cargos que tengan empleados asociados (`ProtectedError`).
- **Filtros:** Se puede filtrar por `estado`, `cargo` y `area` en los listados de empleados.

---
Desarrollado para la prueba de desarrollo para Maxicassa.