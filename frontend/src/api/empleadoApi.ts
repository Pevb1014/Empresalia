import api from "./axios";

export const listarEmpleados = (params = {}) =>
  api.get("empleados/", { params });

export const obtenerEmpleado = (id: string) =>
  api.get(`empleados/${id}/`);

export const crearEmpleado = (data: object) =>
  api.post("empleados/", data);

export const actualizarEmpleado = (id: string, data: object) =>
  api.patch(`empleados/${id}/`, data);

export const eliminarEmpleado = (id: string) =>
  api.delete(`empleados/${id}/`);