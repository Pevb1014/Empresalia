/** Mapea los datos de la API para el componente DataTable */
export function adaptEmpleadoToTable(empleado: any) {
  return {
    id: empleado.id,
    nombre: empleado.nombre,
    cargo: empleado.cargo, // La API en el listado devuelve el nombre del cargo como string
    area: empleado.area,   // La API en el listado devuelve el nombre del área como string
  };
}

/** Mapea el detalle de la API para inicializar el DynamicForm */
export function adaptEmpleadoToForm(empleado: any) {
  return {
    nombre: empleado?.nombre || "",
    numero_documento: empleado?.numero_documento || "",
    correo: empleado?.correo || "",
    fecha_ingreso: empleado?.fecha_ingreso || "",
    estado: empleado?.estado || "ACTIVO",
    cargo: empleado?.cargo?.id || empleado?.cargo || "",
  };
}

/** Convierte los datos del formulario en el DTO que espera el Backend */
export function adaptFormToEmpleadoPayload(formData: Record<string, any>) {
  return {
    nombre: formData.nombre?.trim() || "",
    numero_documento: formData.numero_documento?.trim() || "",
    correo: formData.correo?.trim() || "",
    fecha_ingreso: formData.fecha_ingreso || null,
    estado: formData.estado || "ACTIVO",
    cargo: formData.cargo || null,
  };
}