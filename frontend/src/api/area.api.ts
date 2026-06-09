import api from "./axios";
import type { AreaDetail, AreaWrite, AreaList, AreaFilters } from "../interfaces/area"; 
import type { PaginatedResponse } from "../interfaces/pagination";

export const listarAreas = (params: AreaFilters = {}) =>
  api.get<PaginatedResponse<AreaList>>("areas/", { params });

export const obtenerArea = (id: string) =>
  api.get<AreaDetail>(`areas/${id}/`);

export const crearArea = (data: AreaWrite) =>
  api.post<AreaWrite>("areas/", data);

export const actualizarArea = (
  id: string,
  data: Partial<AreaWrite>
) =>
  api.patch<AreaWrite>(`areas/${id}/`, data);

export const eliminarArea = (id: string) =>
  api.delete(`areas/${id}/`);