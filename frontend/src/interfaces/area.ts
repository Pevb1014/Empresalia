import type { CargoNested } from "./cargo";
import type { PaginationFilters } from "./pagination";

/**
 * Representa un Área Corporativa en listados generales.
 * Corresponde al 'AreaListSerializer' del backend.
 */
export interface AreaList {
  id: string; // UUID
  nombre: string;
}

/**
 * Representa el detalle completo de un Área Corporativa.
 * Incluye relaciones anidadas y campos extendidos.
 * Corresponde al 'AreaDetailSerializer' del backend.
 */
export interface AreaDetail extends AreaList {
  descripcion: string | null;
  /** Lista de cargos que pertenecen exclusivamente a esta área */
  cargos: CargoNested[];
}

/**
 * Estructura necesaria para las operaciones de escritura (POST/PUT/PATCH).
 * Corresponde al 'AreaWriteSerializer' del backend.
 */
export interface AreaWrite {
  nombre: string;
  descripcion?: string | null;
}

export interface AreaFilters extends PaginationFilters {
  ordering?: "nombre" | "-nombre";
}
