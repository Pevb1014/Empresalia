import api from "./axios";

export const listarHistorial = (params = {}) =>
  api.get("historial/", { params });

export const obtenerRegistroHistorial = (
  id: string
) =>
  api.get(`historial/${id}/`);