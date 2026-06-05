export function adaptArea(area: any) {
  return {
    id: area.id,
    nombre: area.nombre,
  };
}

export function adaptAreaToForm(area: any) {
  return {
    nombre: area?.nombre || "",
    descripcion: area?.descripcion || "",
  };
}


export function adaptFormToAreaPayload(formData: Record<string, any>) {
  return {
    nombre: formData.nombre?.trim() || "",
    descripcion: formData.descripcion?.trim() || null, 
  };
}