import api from "./axios";
import type { HistorialDetail, HistorialList, HistorialFilters } from "../interfaces/historial";
import type { PaginatedResponse } from "../interfaces/pagination";

export const listarHistorial = (params: HistorialFilters = {}) =>
  api.get<PaginatedResponse<HistorialList>>("historial/", { params });

export const obtenerRegistroHistorial = (
  id: string
) =>
  api.get<HistorialDetail>(`historial/${id}/`);