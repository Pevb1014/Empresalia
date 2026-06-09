import type { PaginationFilters } from "./pagination";

/**
 * Define los tipos de operaciones que el sistema registra en la auditoría.
 */
export type TipoCambio = "CREACION" | "ACTUALIZACION";


/**
 * Representación de un registro de auditoría en listados.
 * Corresponde al 'HistorialListSerializer' del backend.
 * Proporciona una vista rápida de quién cambió y cuándo.
 */
export interface HistorialList {
    id: string; // UUID
    /** Nombre del empleado afectado */
    empleado: string;
    /** Nombre del cargo del empleado al momento del registro */
    cargo: string;
    /** Nombre del área del empleado al momento del registro */
    area: string;
    /** Fecha y hora del cambio en formato ISO (YYYY-MM-DDTHH:mm:ssZ) */
    fecha_cambio: string;
    tipo_cambio: TipoCambio;
}

/**
 * Representación detallada de un cambio específico.
 * Corresponde al 'HistorialDetailSerializer' del backend.
 * Incluye el rastro exacto de qué valor se modificó.
 */
export interface HistorialDetail extends HistorialList {
    /** Nombre técnico del campo que fue modificado en el modelo */
    campo_cambiado: string;
    /** 
     * Valor previo al cambio. 
     * Es null si el tipo de cambio es 'CREACION'.
     */
    valor_anterior: string | null;
    /** Nuevo valor asignado al campo */
    valor_nuevo: string | null;
}

/**
 * Filtros disponibles para la consulta del historial.
 * Útil para la integración con los parámetros del ViewSet.
 */
export interface HistorialFilters extends PaginationFilters{
    empleado?: string; // UUID
    tipo_cambio?: TipoCambio;
    empleado__cargo?: string; // UUID
    empleado__cargo__area?: string; // UUID
    ordering?: "fecha_cambio" | "-fecha_cambio";
}
