import type { AreaList } from "./area";
import type { CargoNested } from "./cargo";
import type { HistorialList } from "./historial";
import type { PaginationFilters } from "./pagination";

/**
 * Posibles estados operativos de un empleado.
 */
export type EstadoEmpleado = "ACTIVO" | "INACTIVO";

/**
 * Representación mínima de un Empleado para relaciones anidadas.
 * Corresponde al 'EmpleadoNestedSerializer' del backend.
 */
export interface EmpleadoNested {
  id: string; // UUID
  nombre: string;
}

/**
 * Representación de un Empleado en listados generales.
 * Corresponde al 'EmpleadoListSerializer' del backend.
 * Los campos 'area' y 'cargo' vienen como strings (nombres).
 */
export interface EmpleadoList extends EmpleadoNested {
  area: string;
  cargo: string;
}

/**
 * Detalle completo de un Empleado.
 * Corresponde al 'EmpleadoDetailSerializer' del backend.
 * Incluye objetos anidados para Área y Cargo.
 */
export interface EmpleadoDetail extends EmpleadoNested {
  numero_documento: string;
  correo: string;
  cargo: CargoNested;
  area: AreaList;
  /** Fecha en formato ISO (YYYY-MM-DD) */
  fecha_ingreso: string;
  estado: EstadoEmpleado;
  /** Lista de cambios realizados en la ficha del empleado */
  historial_cambios: HistorialList[];
}

/**
 * Estructura para operaciones de escritura (POST/PUT/PATCH).
 * Corresponde al 'EmpleadoWriteSerializer' del backend.
 */
export interface EmpleadoWrite {
  numero_documento: string;
  nombre: string;
  correo: string;
  /** Fecha en formato ISO (YYYY-MM-DD) */
  fecha_ingreso: string;
  estado: EstadoEmpleado;
  /** UUID del cargo al que se asigna */
  cargo: string;
}


export interface EmpleadoFilters extends PaginationFilters{
  estado?: EstadoEmpleado;
  cargo?: string;           // UUID
  area?: string;            // UUID
  ordering?: string;        // Ej: "nombre" o "-fecha_ingreso"
}
