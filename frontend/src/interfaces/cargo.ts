import type { AreaList } from "./area";
import type { EmpleadoNested } from "./empleado";
import type { PaginationFilters } from "./pagination";

/**
 * Representación mínima de un Cargo para relaciones anidadas.
 * Corresponde al 'CargoNestedSerializer' del backend.
 */
export interface CargoNested {
  id: string; // UUID
  nombre: string;
}

/**
 * Representa un Cargo en listados generales.
 * El campo 'area' viene aplanado como un string (nombre del área).
 * Corresponde al 'CargoListSerializer' del backend.
 */
export interface CargoList extends CargoNested {
  area: string;
}

/**
 * Representa el detalle completo de un Cargo.
 * Incluye la relación completa con su área y la descripción.
 * Corresponde al 'CargoDetailSerializer' del backend.
 */
export interface CargoDetail extends CargoNested {
  descripcion: string | null;
  /** Objeto completo del área a la que pertenece */
  area: AreaList;
  /** Lista de empleados que ocupan actualmente este cargo */
  empleados: EmpleadoNested[];
}

/**
 * Estructura para operaciones de escritura (POST/PUT/PATCH).
 * El campo 'area' debe ser el UUID del área.
 * Corresponde al 'CargoWriteSerializer' del backend.
 */
export interface CargoWrite {
  nombre: string;
  descripcion?: string | null;
  /** ID del área (UUID) */
  area: string;
}

export interface CargoFilters extends PaginationFilters{
  area?: string;            // UUID
  ordering?: "nombre" | "-nombre";
}
