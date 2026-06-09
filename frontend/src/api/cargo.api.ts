import api from "./axios";
import type { CargoDetail, CargoWrite, CargoList, CargoFilters } from "../interfaces/cargo";
import type { PaginatedResponse } from "../interfaces/pagination";

export const listarCargos = (params: CargoFilters = {}) =>
  api.get<PaginatedResponse<CargoList>>("cargos/", { params });

export const obtenerCargo = (id: string) =>
  api.get<CargoDetail>(`cargos/${id}/`);

export const crearCargo = (data: CargoWrite) =>
  api.post<CargoWrite>("cargos/", data);

export const actualizarCargo = (
  id: string,
  data: Partial<CargoWrite>
) =>
  api.patch<CargoWrite>(`cargos/${id}/`, data);

export const eliminarCargo = (id: string) =>
  api.delete(`cargos/${id}/`);