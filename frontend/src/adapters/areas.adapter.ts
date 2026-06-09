import type { AreaList, AreaDetail, AreaWrite } from "../interfaces/area";

/** Mapea los datos de la API para el componente DataTable */
export function adaptAreaToTable(area: AreaList) {
  return {
    id: area.id,
    nombre: area.nombre,
  };
}

/** Mapea el detalle de la API para inicializar el DynamicForm */
export function adaptAreaToForm(area?: AreaDetail) {
  return {
    nombre: area?.nombre || "",
    descripcion: area?.descripcion || "",
  };
}

/** Convierte los datos del formulario en el DTO que espera el Backend */
export function adaptFormToAreaPayload(formData: Record<string, any>): AreaWrite {
  return {
    nombre: formData.nombre?.trim() || "",
    descripcion: formData.descripcion?.trim() || null, 
  };
}