import api from "./axios";
import type { EmpleadoDetail, EmpleadoWrite, EmpleadoList, EmpleadoFilters } from "../interfaces/empleado";
import type { PaginatedResponse } from "../interfaces/pagination";

export const listarEmpleados = (params: EmpleadoFilters = {}) =>
  api.get<PaginatedResponse<EmpleadoList>>("empleados/", { params });

export const obtenerEmpleado = (id: string) =>
  api.get<EmpleadoDetail>(`empleados/${id}/`);

export const crearEmpleado = (data: EmpleadoWrite) =>
  api.post<EmpleadoWrite>("empleados/", data);

export const actualizarEmpleado = (
  id: string,
  data: Partial<EmpleadoWrite>
) =>
  api.patch<EmpleadoWrite>(`empleados/${id}/`, data);

export const eliminarEmpleado = (id: string) =>
  api.delete(`empleados/${id}/`);