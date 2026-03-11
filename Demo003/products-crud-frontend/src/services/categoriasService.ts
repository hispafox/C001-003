import fetchJson from "./api";
import type { CategoriaResumen } from "../types/models";

/**
 * Obtiene categorías (GET /api/categories).
 * @param isActive - Filtro opcional por estado activo/inactivo.
 */
export function getCategorias(isActive?: boolean): Promise<CategoriaResumen[]> {
  const params = isActive !== undefined ? `?isActive=${isActive}` : "";
  return fetchJson<CategoriaResumen[]>(`/categories${params}`);
}
