import api from "./axios";

export const listarCargos = (params = {}) =>
  api.get("cargos/", { params });

export const obtenerCargo = (id: string) =>
  api.get(`cargos/${id}/`);

export const crearCargo = (data: object) =>
  api.post("cargos/", data);

export const actualizarCargo = (id: string, data: object) =>
  api.patch(`cargos/${id}/`, data);

export const eliminarCargo = (id: string) =>
  api.delete(`cargos/${id}/`);