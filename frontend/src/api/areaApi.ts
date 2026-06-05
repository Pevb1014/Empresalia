import api from "./axios";

export const listarAreas = (params = {}) =>
  api.get("areas/", { params });

export const obtenerArea = (id: string) =>
  api.get(`areas/${id}/`);

export const crearArea = (data: object) =>
  api.post("areas/", data);

export const actualizarArea = (
  id: string,
  data: object
) =>
  api.patch(`areas/${id}/`, data);

export const eliminarArea = (id: string) =>
  api.delete(`areas/${id}/`);