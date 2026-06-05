export function adaptEmpleado(empleado: any) {
  return {
    id: empleado.id,
    nombre: empleado.nombre,
    apellido: empleado.apellido,
    email: empleado.email,
    cargo: {
      nombre: typeof empleado.cargo === "string"
        ? empleado.cargo
        : (empleado.cargo?.nombre || "Sin cargo asignado")
    }
  };
}

export function adaptEmpleadoToForm(empleado: any) {
  return {
    nombre: empleado?.nombre || "",
    apellido: empleado?.apellido || "",
    email: empleado?.email || "",
    cargo: empleado?.cargo?.id || empleado?.cargo || ""
  };
}

export function adaptFormToEmpleadoPayload(formData: Record<string, any>) {
  return {
    nombre: formData.nombre?.trim() || "",
    apellido: formData.apellido?.trim() || "",
    email: formData.email?.trim() || "",
    cargo: formData.cargo || null
  };
}