import type { CargoList, CargoDetail, CargoWrite } from "../interfaces/cargo";

/** Mapea los datos de la API para el componente DataTable */
export function adaptCargoToTable(cargo: CargoList) {
  return {
    id: cargo.id,
    nombre: cargo.nombre,
    area: cargo.area, // En la lista, la API devuelve el nombre del área como string
  };
}

/** Mapea el detalle de la API para inicializar el DynamicForm */
export function adaptCargoToForm(cargo?: CargoDetail) {
  return {
    nombre: cargo?.nombre || "",
    descripcion: cargo?.descripcion || "",
    area: cargo?.area?.id || "", // En el detalle, area es un objeto anidado
  };
}

/** Convierte los datos del formulario en el DTO que espera el Backend */
export function adaptFormToCargoPayload(formData: Record<string, any>): CargoWrite {
  return {
    nombre: formData.nombre?.trim() || "",
    descripcion: formData.descripcion?.trim() || null,
    area: formData.area || null,
  };
}