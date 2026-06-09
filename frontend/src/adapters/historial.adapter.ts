/** Mapea los datos de la API para el componente DataTable del historial */
export function adaptHistorialToTable(item: any) {
  return {
    id: item.id,
    empleado: item.empleado,
    tipo: item.tipo_cambio,
    fecha: item.fecha_cambio
  };
}

/** Mapea el detalle de un registro de auditoría */
export function adaptHistorialToDetail(item: any) {
  return {
    ...item,
    fecha: item.fecha_cambio,
    tipo: item.tipo_cambio,
    campo: item.campo_cambiado
  };
}