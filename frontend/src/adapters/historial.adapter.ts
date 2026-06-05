export function adaptHistorial(item: any) {
  return {
    id: item.id,
    accion: item.accion,
    descripcion: item.descripcion,
    fecha: item.fecha
  };
}