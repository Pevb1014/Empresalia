export function adaptCargo(cargo: any) {
  return {
    id: cargo?.id,
    nombre: cargo?.nombre,
    area: {
      nombre: cargo?.area,
    },
  };
}

export function adaptCargoToForm(cargo: any) {
  return {
    nombre: cargo?.nombre || "",
    area: cargo?.area?.id || cargo?.area || "",
  };
}

export function adaptFormToCargoPayload(formData: Record<string, any>) {
  return {
    nombre: formData.nombre?.trim() || "",
    area: formData.area || null, 
  };
}